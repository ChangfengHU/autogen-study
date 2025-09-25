from __future__ import annotations

from typing import Any, Hashable

from .component import Component, WeatherServiceConfig
from .mixins import CacheMixin, RateLimitMixin, ServiceBase
from .provider import WeatherProvider


class WeatherBackend(ServiceBase):
    """具体后端：委托给 WeatherProvider 获取数据。

    该类位于 MRO 底部，使得各个 mixin 通过 ``super().fetch`` 最终落到这里取真实数据。
    """

    def __init__(self, provider: WeatherProvider) -> None:
        # ServiceBase 没有状态，这里无需 super()；保持简单
        self._provider = provider

    def fetch(self, key: Hashable) -> Any:
        # 统一将 key 视为城市名称字符串
        city = str(key)
        return self._provider.get_weather(city)


class WeatherService(CacheMixin, RateLimitMixin, Component[WeatherServiceConfig], WeatherBackend):
    """通过多继承组合行为的天气服务。

    顺序很重要（最左侧的 mixin 最先运行）：
    CacheMixin -> RateLimitMixin -> Component[Config] -> WeatherBackend
    """

    def __init__(self, provider: WeatherProvider, config: WeatherServiceConfig) -> None:
        # 为了示例清晰，这里显式初始化所有基类；
        # 在大型代码库中，若各基类已设计为可协作，优先使用 super() 协作初始化。
        CacheMixin.__init__(self)
        RateLimitMixin.__init__(self)
        Component.__init__(self, config)
        WeatherBackend.__init__(self, provider)
