from __future__ import annotations

import time
from collections import deque
from typing import Any, Deque, Dict, Hashable, Tuple


class ServiceBase:
    """Abstract service protocol for mixins to cooperate via super().

    Subclasses should override ``fetch(key: Hashable) -> Any``.
    """

    def fetch(self, key: Hashable) -> Any:  # pragma: no cover - interface only
        raise NotImplementedError


class CacheMixin(ServiceBase):
    """Simple TTL cache mixin.

    Expects ``self.config.cache_ttl_seconds`` to exist (provided by a config-holding base).
    """

    def __init__(self) -> None:
        # Mixin keeps init self-contained to avoid forcing cooperative super() chains.
        self._cache: Dict[Hashable, Tuple[float, Any]] = {}

    def fetch(self, key: Hashable) -> Any:
        now = time.time()
        ttl = getattr(self.config, "cache_ttl_seconds", 0)
        if ttl > 0:
            hit = self._cache.get(key)
            if hit is not None:
                expires_at, value = hit
                if expires_at > now:
                    return value

        value = super().fetch(key)
        if ttl > 0:
            self._cache[key] = (now + ttl, value)
        return value


class RateLimitMixin(ServiceBase):
    """Simple per-minute rolling window rate limiter mixin.

    Expects ``self.config.rate_limit_per_minute`` to exist.
    """

    def __init__(self) -> None:
        # Mixin keeps init self-contained to avoid forcing cooperative super() chains.
        self._calls: Deque[float] = deque()

    def fetch(self, key: Hashable) -> Any:
        limit = getattr(self.config, "rate_limit_per_minute", 0)
        if limit > 0:
            now = time.time()
            window_start = now - 60.0
            # discard old calls
            while self._calls and self._calls[0] < window_start:
                self._calls.popleft()
            if len(self._calls) >= limit:
                raise RuntimeError("Rate limit exceeded")
            self._calls.append(now)
        return super().fetch(key)
