from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

TConfig = TypeVar("TConfig")


class Component(Generic[TConfig]):
    """泛型组件基类，持有强类型配置。"""

    def __init__(self, config: TConfig) -> None:
        self.config: TConfig = config


@dataclass(slots=True)
class StudentConfig:
    """学生角色的强类型配置。

    属性：
        max_courses: 学生可被评分的不同科目上限。
    """

    max_courses: int = 4


@dataclass(slots=True)
class TeacherConfig:
    """教师角色的强类型配置。

    属性：
        department: 所在学院/部门名称。
    """

    department: str = "Math"
