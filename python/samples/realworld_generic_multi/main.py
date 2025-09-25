from __future__ import annotations

from .component import WeatherServiceConfig
from .provider import MockWeatherProvider
from .service import WeatherService


def demo() -> None:
    provider = MockWeatherProvider()
    config = WeatherServiceConfig(cache_ttl_seconds=5, rate_limit_per_minute=3)
    service = WeatherService(provider, config)

    cities = ["Shanghai", "Shanghai", "Beijing", "Shanghai"]

    print("== Requests (cache in action, limit preserved) ==")
    for i, city in enumerate(cities, 1):
        try:
            result = service.fetch(city)
            print(f"{i}. {city} -> {result}")
        except Exception as e:  # noqa: BLE001 (demo output)
            print(f"{i}. {city} -> ERROR: {e}")

    print("\n== Requests (force rate limit by varying keys) ==")
    # Reset service to isolate counters from the previous phase.
    service = WeatherService(provider, config)
    varying = ["A", "B", "C", "D"]  # 4 unique -> limit is 3, expect 4th to fail
    for i, city in enumerate(varying, 1):
        try:
            result = service.fetch(city)
            print(f"{i}. {city} -> {result}")
        except Exception as e:  # noqa: BLE001 (demo output)
            print(f"{i}. {city} -> ERROR: {e}")

    print("\n== MRO (Method Resolution Order) ==")
    for cls in WeatherService.mro():
        print(cls.__name__)

    print("\n== Typed Config ==")
    print(service.config)


if __name__ == "__main__":
    demo()
