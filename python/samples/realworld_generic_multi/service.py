from __future__ import annotations

from typing import Any, Hashable

from .component import Component, WeatherServiceConfig
from .mixins import CacheMixin, RateLimitMixin, ServiceBase
from .provider import WeatherProvider


class WeatherBackend(ServiceBase):
    """Concrete backend that delegates to a WeatherProvider.

    This sits at the bottom of the MRO so that mixins can call ``super().fetch``
    and eventually land here to retrieve the actual data.
    """

    def __init__(self, provider: WeatherProvider) -> None:
        super().__init__()
        self._provider = provider

    def fetch(self, key: Hashable) -> Any:
        city = str(key)
        return self._provider.get_weather(city)


class WeatherService(CacheMixin, RateLimitMixin, Component[WeatherServiceConfig], WeatherBackend):
    """Weather service combining behaviors via multiple inheritance.

    Order matters (left-most mixin runs first):
    CacheMixin -> RateLimitMixin -> Component[Config] -> WeatherBackend
    """

    def __init__(self, provider: WeatherProvider, config: WeatherServiceConfig) -> None:
        # Initialize all bases explicitly for clarity; in large codebases, prefer cooperative
        # __init__ with super() if bases are designed for it.
        CacheMixin.__init__(self)
        RateLimitMixin.__init__(self)
        Component.__init__(self, config)
        WeatherBackend.__init__(self, provider)

