from __future__ import annotations

from typing import List, Optional, Tuple


class ChatCompletionContext:
    """Simple chat context that stores (role, content) messages.

    Designed as a reusable base that can be combined via multiple inheritance
    with other mixins/components.
    """

    def __init__(self) -> None:
        self._messages: List[Tuple[str, str]] = []

    def add_message(self, role: str, content: str) -> None:
        """Append a message to the conversation history."""
        self._messages.append((role, content))

    def last_user_message(self) -> Optional[str]:
        """Return the most recent user message, if any."""
        for role, content in reversed(self._messages):
            if role == "user":
                return content
        return None

    def render_history(self) -> str:
        """Return the history as a displayable string."""
        return "\n".join(f"{r}: {c}" for r, c in self._messages)

