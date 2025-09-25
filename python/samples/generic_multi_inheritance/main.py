from __future__ import annotations

from .unbounded_context import (
    UnboundedChatCompletionContext,
    UnboundedChatCompletionContextConfig,
)


def demo() -> None:
    cfg = UnboundedChatCompletionContextConfig(max_messages=5, system_prompt="Be concise.")
    ctx = UnboundedChatCompletionContext(cfg)

    ctx.add_message("user", "你好，帮我总结下多继承 + 范型的好处？")
    ctx.add_message("assistant", "多继承用于组合功能；范型提供类型安全的配置。")
    ctx.add_message("user", "给个简单例子吧。")

    print("== Rendered History ==")
    print(ctx.render_history())

    print("\n== Last User Message ==")
    print(ctx.last_user_message())

    print("\n== Config Type & Value ==")
    # IDEs/type-checkers know cfg fields; autocompletion and type checks apply.
    print(type(ctx.config).__name__, ctx.config)

    print("\n== MRO (Method Resolution Order) ==")
    for cls in UnboundedChatCompletionContext.mro():
        print(cls.__name__)


if __name__ == "__main__":
    demo()

