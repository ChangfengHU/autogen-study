from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

TConfig = TypeVar("TConfig")


class Component(Generic[TConfig]):
    """Generic component that holds a strongly-typed configuration.

    Using ``Component[TConfig]`` gives type checkers and IDEs visibility into
    configuration structure across the codebase.
    """

    def __init__(self, config: TConfig) -> None:
        self.config: TConfig = config


@dataclass(slots=True)
class WeatherServiceConfig:
    """Typed config for WeatherService.

    Attributes:
        cache_ttl_seconds: TTL for cache entries.
        rate_limit_per_minute: Allowed operations per rolling minute.
    """

    cache_ttl_seconds: int = 10
    rate_limit_per_minute: int = 5

