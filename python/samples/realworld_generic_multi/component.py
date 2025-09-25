from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

TConfig = TypeVar("TConfig")


class Component(Generic[TConfig]):
    """泛型组件基类，持有强类型配置。

    使用 ``Component[TConfig]`` 能让类型检查器与 IDE 理解配置结构，
    在整个代码库范围获得更好的提示与校验。
    """

    def __init__(self, config: TConfig) -> None:
        self.config: TConfig = config


@dataclass(slots=True)
class WeatherServiceConfig:
    """天气服务的强类型配置。

    属性：
        cache_ttl_seconds: 缓存条目的生存时间（秒）。
        rate_limit_per_minute: 每分钟允许的请求次数（滚动窗口）。
    """

    cache_ttl_seconds: int = 10
    rate_limit_per_minute: int = 5
