Real-World: WeatherService (Generics + Multiple Inheritance)

Scenario
- A weather service that needs: typed configuration, caching to avoid repeated calls, and rate limiting to protect an upstream API.
- We implement this by composing behaviors with multiple inheritance and keeping the configuration strongly typed via generics.

Files
- component.py: Generic Component[TConfig] base, holds typed config and lifecycle.
- mixins.py: CacheMixin and RateLimitMixin implement reusable cross‑cutting behavior.
- provider.py: WeatherProvider interface and a MockWeatherProvider.
- service.py: WeatherService(CacheMixin, RateLimitMixin, Component[WeatherServiceConfig], WeatherBackend).
- main.py: Runnable demo showing cache hits and rate‑limit behavior.

Benefits of this design
- Separation of concerns: cache和限流各自作为 mixin，可在其他服务中重用；业务取数逻辑仅在 WeatherBackend。
- 强类型配置（泛型）：Component[WeatherServiceConfig] 让配置项在 IDE/mypy/pyright 下有补全与校验，降低配置错误。
- 可组合的行为：通过多继承按顺序叠加行为（MRO 左到右），如先限流再缓存或先缓存再限流，根据需求调整顺序即可。
- 易于测试：mixin 可单测；MockProvider 便于端到端验证而无需真实网络。

Run
- From repo root:
  - python -m python.samples.realworld_generic_multi.main

