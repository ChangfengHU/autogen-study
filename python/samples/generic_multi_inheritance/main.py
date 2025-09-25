from __future__ import annotations

from .unbounded_context import (
    UnboundedChatCompletionContext,
    UnboundedChatCompletionContextConfig,
)


def demo() -> None:
    # 配置允许最多保留 5 条消息，并添加系统提示词
    cfg = UnboundedChatCompletionContextConfig(max_messages=5, system_prompt="Be concise.")
    ctx = UnboundedChatCompletionContext(cfg)

    ctx.add_message("user", "你好，帮我总结下多继承 + 范型的好处？")
    ctx.add_message("assistant", "多继承用于组合功能；范型提供类型安全的配置。")
    ctx.add_message("user", "给个简单例子吧。")

    # 展示历史与最近一条用户消息
    print("== Rendered History ==")
    print(ctx.render_history())

    print("\n== Last User Message ==")
    print(ctx.last_user_message())

    print("\n== Config Type & Value ==")
    # IDEs/type-checkers know cfg fields; autocompletion and type checks apply.
    print(type(ctx.config).__name__, ctx.config)

    # 打印方法解析顺序（左到右优先）
    print("\n== MRO (Method Resolution Order) ==")
    for cls in UnboundedChatCompletionContext.mro():
        print(cls.__name__)


if __name__ == "__main__":
    demo()
