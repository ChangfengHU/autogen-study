from __future__ import annotations

from dataclasses import dataclass

from .component import Component
from .context_base import ChatCompletionContext


@dataclass(slots=True)
class UnboundedChatCompletionContextConfig:
    """Configuration for UnboundedChatCompletionContext.

    Attributes:
        max_messages: Soft cap for messages kept in memory.
        system_prompt: Optional system prompt to prepend (if any).
    """

    max_messages: int = 1000
    system_prompt: str = "You are a helpful assistant."


class UnboundedChatCompletionContext(
    ChatCompletionContext, Component[UnboundedChatCompletionContextConfig]
):
    """A context that is both a chat context and a generic component.

    Demonstrates multiple inheritance with a parameterized base class:
    - ChatCompletionContext provides message history utilities.
    - Component[UnboundedChatCompletionContextConfig] provides a typed config and lifecycle.
    """

    def __init__(self, config: UnboundedChatCompletionContextConfig) -> None:
        # Initialize both bases explicitly for clarity in this sample.
        ChatCompletionContext.__init__(self)
        Component.__init__(self, config)

        if config.system_prompt:
            self.add_message("system", config.system_prompt)

    def add_message(self, role: str, content: str) -> None:
        """Append while respecting the max_messages cap from config."""
        super().add_message(role, content)
        # Trim history softly if we exceed the configured cap.
        overflow = len(self._messages) - self.config.max_messages
        if overflow > 0:
            del self._messages[0:overflow]

