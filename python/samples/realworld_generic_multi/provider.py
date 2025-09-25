from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class WeatherProvider(Protocol):
    """Protocol for a weather data backend."""

    def get_weather(self, city: str) -> str:  # simplified for the demo
        ...


@dataclass(slots=True)
class MockWeatherProvider:
    """A mock provider returning deterministic strings (no network)."""

    def get_weather(self, city: str) -> str:
        return f"Sunny 25°C in {city}"

