from __future__ import annotations

from .component import WeatherServiceConfig
from .provider import MockWeatherProvider
from .service import WeatherService


def demo() -> None:
    provider = MockWeatherProvider()
    # 缓存 5 秒；限流 3 次/分钟
    config = WeatherServiceConfig(cache_ttl_seconds=5, rate_limit_per_minute=3)
    service = WeatherService(provider, config)

    # 同一城市多次请求，应有缓存命中
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
    # 重置服务以清空计数器；随后用 4 个不同城市触发限流
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
