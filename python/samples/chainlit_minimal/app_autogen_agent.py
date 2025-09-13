import os
from pathlib import Path

import chainlit as cl
import yaml
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_core.models import ChatCompletionClient


def _load_model_config_from_env_or_file(base_dir: str) -> dict:
    """Load model config from MODEL_CONFIG (YAML), MODEL_CONFIG_PATH, or default model_config.yaml near this file.

    Supports environment-only configuration for OpenAI/Azure when file is absent.
    """
    inline_yaml = os.getenv("MODEL_CONFIG")
    if inline_yaml:
        return yaml.safe_load(inline_yaml)

    cfg_path = os.getenv("MODEL_CONFIG_PATH", str(Path(base_dir) / "model_config.yaml"))
    if os.path.exists(cfg_path):
        with open(cfg_path, "r") as f:
            return yaml.safe_load(f)

    # Env-only fallback: OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o")
        return {
            "provider": "autogen_ext.models.openai.OpenAIChatCompletionClient",
            "config": {"model": model_name, "api_key": openai_key},
        }

    # Env-only fallback: Azure OpenAI
    azure_ep = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_ver = os.getenv("AZURE_OPENAI_API_VERSION")
    azure_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_dep = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    if azure_ep and azure_ver and (azure_key or os.getenv("AZURE_AD_TOKEN")):
        cfg: dict = {
            "provider": "autogen_ext.models.openai.AzureOpenAIChatCompletionClient",
            "config": {
                "model": os.getenv("OPENAI_MODEL", "gpt-4o"),
                "azure_endpoint": azure_ep,
                "api_version": azure_ver,
            },
        }
        if azure_dep:
            cfg["config"]["azure_deployment"] = azure_dep
        if azure_key:
            cfg["config"]["api_key"] = azure_key
        return cfg

    raise FileNotFoundError(
        "No model configuration found. Provide MODEL_CONFIG (YAML), set MODEL_CONFIG_PATH/model_config.yaml, "
        "or set envs OPENAI_API_KEY (and optional OPENAI_MODEL) or Azure envs."
    )


@cl.on_chat_start
async def on_start() -> None:
    """Initialize AssistantAgent and store in session."""
    # Optional: connect to PyCharm Debug Server if requested
    # Enable by: export PYCHARM_DEBUG=1 (and start a Python Debug Server in PyCharm on PYCHARM_DEBUG_PORT, default 53100)
    if os.getenv("PYCHARM_DEBUG") == "1":
        try:
            import pydevd_pycharm  # type: ignore

            port = int(os.getenv("PYCHARM_DEBUG_PORT", "53100"))
            pydevd_pycharm.settrace(
                "localhost",
                port=port,
                stdoutToServer=True,
                stderrToServer=True,
                suspend=False,
            )
            print(f"[pydevd] Connected to PyCharm Debug Server on port {port}")
        except Exception as e:
            print(f"[pydevd] Debug attach failed: {e}")
    base_dir = os.path.dirname(__file__)
    model_config = _load_model_config_from_env_or_file(base_dir)
    model_client = ChatCompletionClient.load_component(model_config)

    agent = AssistantAgent(
        name="assistant",
        model_client=model_client,
        system_message="You are a helpful assistant.",
        # 这里用非流式，逻辑更简单。需要流式可设置 model_client_stream=True 并改用 on_messages_stream。
    )
    cl.user_session.set("agent", agent)  # type: ignore


@cl.on_message
async def on_message(message: cl.Message) -> None:
    agent = cl.user_session.get("agent")  # type: ignore
    if not isinstance(agent, AssistantAgent):
        await cl.Message(content="Agent not initialized.").send()
        return

    response = await agent.on_messages(
        messages=[TextMessage(content=message.content, source="user")],
        cancellation_token=CancellationToken(),
    )

    if response and response.chat_message and isinstance(response.chat_message, TextMessage):
        await cl.Message(content=response.chat_message.content).send()
    else:
        await cl.Message(content="No text response from agent.").send()
