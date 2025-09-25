from __future__ import annotations

import time
from collections import deque
from typing import Any, Deque, Dict, Hashable, Tuple


class ServiceBase:
    """抽象服务协议：为 mixin 通过 super() 协作预留接口。

    子类应实现 ``fetch(key: Hashable) -> Any``。
    """

    def fetch(self, key: Hashable) -> Any:  # pragma: no cover - interface only
        raise NotImplementedError


class CacheMixin(ServiceBase):
    """简单的 TTL 缓存 Mixin。

    期望存在 ``self.config.cache_ttl_seconds``（由持有配置的基类提供）。
    """

    def __init__(self) -> None:
        # Mixin 的初始化尽量自洽，避免强制整个继承链必须 super() 协作。
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
    """简单的“每分钟滚动窗口”限流 Mixin。

    期望存在 ``self.config.rate_limit_per_minute``。
    """

    def __init__(self) -> None:
        # Mixin 的初始化尽量自洽，避免强制整个继承链必须 super() 协作。
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
                raise RuntimeError("超过每分钟限流阈值")
            self._calls.append(now)
        return super().fetch(key)
