现实场景示例：天气服务（泛型 + 多继承）

场景
- 天气服务需要三种能力：强类型配置、缓存（减少重复请求）、限流（保护上游接口）。
- 通过“多继承”把可复用的行为（Mixin）叠加到具体服务上，并用“泛型”保证配置类型安全。

文件
- component.py：泛型组件基类 Component[TConfig]，持有强类型配置。
- mixins.py：CacheMixin（TTL 缓存）、RateLimitMixin（每分钟限流）。
- provider.py：WeatherProvider 协议与 MockWeatherProvider（无需网络）。
- service.py：WeatherService(CacheMixin, RateLimitMixin, Component[WeatherServiceConfig], WeatherBackend)。
- main.py：可运行演示，展示缓存命中与限流效果。

这么做的好处
- 关注点分离：缓存/限流与业务取数解耦；Mixin 可在其他服务中复用。
- 强类型配置（泛型）：Component[WeatherServiceConfig] 让配置在 IDE/mypy/pyright 下有补全与静态校验。
- 行为可组合：按 MRO（从左到右）叠加行为，可灵活选择“先缓存后限流”或“先限流后缓存”。
- 易测试：Mixin 可单测；MockProvider 支持端到端演示，无需外部依赖。

运行
- 在仓库根目录执行：
  - python -m python.samples.realworld_generic_multi.main

