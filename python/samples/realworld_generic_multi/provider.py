from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class WeatherProvider(Protocol):
    """天气数据后端的协议（接口）。"""

    def get_weather(self, city: str) -> str:  # simplified for the demo
        ...


@dataclass(slots=True)
class MockWeatherProvider:
    """返回可预测字符串的模拟提供者（无需网络）。"""

    def get_weather(self, city: str) -> str:
        return f"Sunny 25°C in {city}"
