from __future__ import annotations

from .component import WeatherServiceConfig
from .provider import MockWeatherProvider
from .service import WeatherService


def demo() -> None:
    provider = MockWeatherProvider()
    config = WeatherServiceConfig(cache_ttl_seconds=5, rate_limit_per_minute=3)
    service = WeatherService(provider, config)

    cities = ["Shanghai", "Shanghai", "Beijing", "Shanghai"]

    print("== 请求（缓存生效，仍保留限流） ==")
    for i, city in enumerate(cities, 1):
        try:
            result = service.fetch(city)
            print(f"{i}. {city} -> {result}")
        except Exception as e:  # noqa: BLE001 (demo output)
            print(f"{i}. {city} -> 错误: {e}")

    print("\n== 请求（更换不同城市以触发限流） ==")
    # Reset service to isolate counters from the previous phase.
    service = WeatherService(provider, config)
    varying = ["A", "B", "C", "D"]  # 4 unique -> limit is 3, expect 4th to fail
    for i, city in enumerate(varying, 1):
        try:
            result = service.fetch(city)
            print(f"{i}. {city} -> {result}")
        except Exception as e:  # noqa: BLE001 (demo output)
            print(f"{i}. {city} -> 错误: {e}")

    print("\n== MRO（方法解析顺序） ==")
    for cls in WeatherService.mro():
        print(cls.__name__)

    print("\n== 强类型配置 ==")
    print(service.config)


if __name__ == "__main__":
    demo()
