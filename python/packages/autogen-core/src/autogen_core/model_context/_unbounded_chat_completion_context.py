from typing import List

from pydantic import BaseModel
from typing_extensions import Self

from .._component_config import Component
from ..models import LLMMessage
from ._chat_completion_context import ChatCompletionContext


class UnboundedChatCompletionContextConfig(BaseModel):
    initial_messages: List[LLMMessage] | None = None

class UnboundedChatCompletionContext(ChatCompletionContext, Component[UnboundedChatCompletionContextConfig]):
    """一个无界聊天补全上下文，保留所有消息的视图。"""

    component_config_schema = UnboundedChatCompletionContextConfig
    component_provider_override = "autogen_core.model_context.UnboundedChatCompletionContext"

    async def get_messages(self) -> List[LLMMessage]:
        """获取最多 `buffer_size` 条最近消息。"""
        return self._messages

    def _to_config(self) -> UnboundedChatCompletionContextConfig:
        return UnboundedChatCompletionContextConfig(initial_messages=self._initial_messages)

    @classmethod
    def _from_config(cls, config: UnboundedChatCompletionContextConfig) -> Self:
        return cls(initial_messages=config.initial_messages)