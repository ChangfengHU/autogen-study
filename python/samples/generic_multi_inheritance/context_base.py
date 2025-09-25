from __future__ import annotations

from typing import List, Optional, Tuple


class ChatCompletionContext:
    """简单的对话上下文，保存 (role, content) 消息。

    作为可复用基类，可通过多继承与其他 Mixin/组件组合使用。
    """

    def __init__(self) -> None:
        # 保存 (角色, 内容) 的简单消息历史
        self._messages: List[Tuple[str, str]] = []

    def add_message(self, role: str, content: str) -> None:
        """追加一条消息到对话历史。"""
        self._messages.append((role, content))

    def last_user_message(self) -> Optional[str]:
        """返回最近一条用户消息（若存在）。"""
        # 逆序扫描，遇到第一条 user 即返回
        for role, content in reversed(self._messages):
            if role == "user":
                return content
        return None

    def render_history(self) -> str:
        """将历史渲染为可阅读的字符串。"""
        return "\n".join(f"{r}: {c}" for r, c in self._messages)
