import os
import chainlit as cl
from openai import OpenAI


# 需要：pip install -U openai
# 并设置环境变量：export OPENAI_API_KEY=你的key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))


@cl.on_message
async def on_message(message: cl.Message) -> None:
    """最小 OpenAI 对话示例。"""
    if not os.environ.get("OPENAI_API_KEY"):
        await cl.Message(content="Missing OPENAI_API_KEY env var.").send()
        return

    resp = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message.content},
        ],
    )
    content = resp.choices[0].message.content
    await cl.Message(content=content).send()
