from __future__ import annotations

from dataclasses import dataclass

from .component import Component
from .context_base import ChatCompletionContext


@dataclass(slots=True)
class UnboundedChatCompletionContextConfig:
    """UnboundedChatCompletionContext 的配置。

    属性：
        max_messages: 内存中保留消息的软上限。
        system_prompt: 可选的系统提示词，会作为第一条消息插入。
    """

    max_messages: int = 1000
    system_prompt: str = "You are a helpful assistant."


class UnboundedChatCompletionContext(
    ChatCompletionContext, Component[UnboundedChatCompletionContextConfig]
):
    """同时具备对话上下文与泛型组件能力的上下文类。

    展示了“带类型参数的基类”的多继承：
    - ChatCompletionContext 提供消息历史相关的方法；
    - Component[UnboundedChatCompletionContextConfig] 提供强类型配置与生命周期能力。
    """

    def __init__(self, config: UnboundedChatCompletionContextConfig) -> None:
        # 本示例中显式初始化两个基类，便于读者理解。
        ChatCompletionContext.__init__(self)
        Component.__init__(self, config)

        if config.system_prompt:
            self.add_message("system", config.system_prompt)

    def add_message(self, role: str, content: str) -> None:
        """追加消息并遵守配置中的 max_messages 上限。"""
        super().add_message(role, content)
        # 超出上限时从头部裁剪，保持软上限。
        overflow = len(self._messages) - self.config.max_messages
        if overflow > 0:
            del self._messages[0:overflow]
