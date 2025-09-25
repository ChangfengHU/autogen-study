from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

TConfig = TypeVar("TConfig")


class Component(Generic[TConfig]):
    """Generic component base that owns a typed config and lifecycle.

    The generic parameter ``TConfig`` enables strong typing of the configuration
    object across the codebase (type checkers, IDEs, and docs benefit).
    """

    def __init__(self, config: TConfig) -> None:
        self.config: TConfig = config
        self._started: bool = False

    def start(self) -> None:
        """Start the component lifecycle."""
        self._started = True

    def stop(self) -> None:
        """Stop the component lifecycle."""
        self._started = False


@dataclass(slots=True)
class BaseEmptyConfig:
    """Convenience empty config for quick demos/tests."""

