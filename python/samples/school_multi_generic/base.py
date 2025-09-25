from __future__ import annotations


class PersonBase:
    """教师/学生共享的人物基础属性。"""

    def __init__(self, name: str) -> None:
        self.name = name
