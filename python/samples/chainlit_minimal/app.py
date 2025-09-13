import chainlit as cl


@cl.on_message
async def on_message(message: cl.Message) -> None:
    """最小回声示例：原样返回用户输入。"""
    await cl.Message(content=f"You said: {message.content}").send()
