import json
import os
from typing import Any

import aiofiles
import yaml
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_core.models import ChatCompletionClient, ModelFamily, ModelInfo
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Serve static files
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def root():
    """Serve the chat interface HTML file."""
    return FileResponse("app_agent.html")

model_config_path = os.getenv("MODEL_CONFIG_PATH", "model_config.yaml")
state_path = "agent_state.json"
history_path = "agent_history.json"


def _json_default(o: Any) -> Any:
    """JSON serializer for special types (e.g., datetime)."""
    # Pydantic v2 dumps datetimes in mode="json"; ensure fallback for plain dicts
    try:
        from datetime import datetime

        if isinstance(o, datetime):
            return o.isoformat()
    except Exception:
        pass
    # Let json raise for unsupported types to surface issues early
    raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")


def _load_model_config_from_env() -> dict[str, Any] | None:
    """Build a model client config from environment variables if possible.

    Priority:
    1) Azure OpenAI via env (AZURE_* vars)
    2) OpenAI via env (OPENAI_API_KEY)
    3) MODEL_CONFIG (YAML string)
    """

    # If YAML is provided directly via env.
    yaml_inline = os.getenv("MODEL_CONFIG")
    if yaml_inline:
        try:
            return yaml.safe_load(yaml_inline)
        except Exception:
            pass

    # Azure OpenAI via env vars.
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    if azure_endpoint and azure_api_version and (azure_api_key or os.getenv("AZURE_AD_TOKEN")):
        # Default model name can be provided via OPENAI_MODEL; otherwise gpt-4o
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o")
        cfg: dict[str, Any] = {
            "provider": "autogen_ext.models.openai.AzureOpenAIChatCompletionClient",
            "config": {
                "model": model_name,
                "azure_endpoint": azure_endpoint,
                "api_version": azure_api_version,
            },
        }
        if azure_deployment:
            cfg["config"]["azure_deployment"] = azure_deployment
        if azure_api_key:
            cfg["config"]["api_key"] = azure_api_key
        return cfg

    # OpenAI via env var.
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o")
        return {
            "provider": "autogen_ext.models.openai.OpenAIChatCompletionClient",
            "config": {
                "model": model_name,
                # api_key optional if OPENAI_API_KEY is set; include for clarity
                "api_key": openai_key,
            },
        }

    return None


async def get_agent() -> AssistantAgent:
    """Get the assistant agent, load state from file."""
    # Get model client from config file or environment.
    if os.path.exists(model_config_path):
        async with aiofiles.open(model_config_path, "r") as file:
            model_config = yaml.safe_load(await file.read())
    else:
        model_config = _load_model_config_from_env()
        if model_config is None:
            raise FileNotFoundError(
                f"model_config.yaml not found at '{model_config_path}', and no suitable environment variables were detected. "
                "Either create a model_config.yaml (see model_config_template.yaml) or set env vars such as OPENAI_API_KEY "
                "(and optional OPENAI_MODEL), or Azure envs: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT."
            )
    # Try to ensure model_info for custom/unknown model names (e.g., Azure deployment aliases)
    try:
        provider = (model_config or {}).get("provider", "")
        cfg = (model_config or {}).get("config", {})
        model_name = cfg.get("model")
        if (
            isinstance(provider, str)
            and ".openai." in provider
            and isinstance(cfg, dict)
            and isinstance(model_name, str)
            and "model_info" not in cfg
        ):
            def _infer_model_info(name: str) -> ModelInfo:
                n = name.lower()
                info: ModelInfo = {
                    "vision": True,
                    "function_calling": True,
                    "json_output": True,
                    "family": ModelFamily.GPT_4O,
                    "structured_output": True,
                    "multiple_system_messages": True,
                }
                if any(k in n for k in ["o4", "gpt-4.5"]):
                    info["family"] = ModelFamily.O4
                elif "o3" in n:
                    info["family"] = ModelFamily.O3
                    if "mini" in n:
                        info["vision"] = False
                elif "o1" in n:
                    info["family"] = ModelFamily.O1
                    info["json_output"] = False
                    info["structured_output"] = True
                elif "gpt-4o" in n:
                    info["family"] = ModelFamily.GPT_4O
                elif "gpt-4" in n:
                    info["family"] = ModelFamily.GPT_4
                elif "gpt-3.5" in n or "gpt-35" in n:
                    info["family"] = ModelFamily.GPT_35
                    info["vision"] = False
                    info["structured_output"] = False
                else:
                    info["family"] = ModelFamily.UNKNOWN
                return info

            cfg["model_info"] = _infer_model_info(model_name)
    except Exception:
        pass

    model_client = ChatCompletionClient.load_component(model_config)
    # Create the assistant agent.
    agent = AssistantAgent(
        name="assistant",
        model_client=model_client,
        system_message="You are a helpful assistant.",
    )
    # Load state from file.
    if not os.path.exists(state_path):
        return agent  # Return agent without loading state.
    async with aiofiles.open(state_path, "r") as file:
        state = json.loads(await file.read())
    await agent.load_state(state)
    return agent


async def get_history() -> list[dict[str, Any]]:
    """Get chat history from file."""
    if not os.path.exists(history_path):
        return []
    async with aiofiles.open(history_path, "r") as file:
        return json.loads(await file.read())


@app.get("/history")
async def history() -> list[dict[str, Any]]:
    try:
        return await get_history()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/chat", response_model=TextMessage)
async def chat(request: TextMessage) -> TextMessage:
    try:
        # Get the agent and respond to the message.
        agent = await get_agent()
        response = await agent.on_messages(messages=[request], cancellation_token=CancellationToken())

        # Save agent state to file (ensure JSON-serializable).
        state = await agent.save_state()
        async with aiofiles.open(state_path, "w") as file:
            await file.write(json.dumps(state, default=_json_default))

        # Save chat history to file.
        history = await get_history()
        # Use BaseMessage.dump() which converts datetimes to JSON-safe
        history.append(request.dump())
        history.append(response.chat_message.dump())
        async with aiofiles.open(history_path, "w") as file:
            await file.write(json.dumps(history, default=_json_default))

        assert isinstance(response.chat_message, TextMessage)
        return response.chat_message
    except Exception as e:
        error_message = {
            "type": "error",
            "content": f"Error: {str(e)}",
            "source": "system"
        }
        raise HTTPException(status_code=500, detail=error_message) from e


# Example usage
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
