from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

TConfig = TypeVar("TConfig")


class Component(Generic[TConfig]):
    """Generic component base holding a strongly-typed config."""

    def __init__(self, config: TConfig) -> None:
        self.config: TConfig = config


@dataclass(slots=True)
class StudentConfig:
    """Typed configuration for Student roles.

    Attributes:
        max_courses: Maximum distinct courses a student can be graded on.
    """

    max_courses: int = 4


@dataclass(slots=True)
class TeacherConfig:
    """Typed configuration for Teacher roles.

    Attributes:
        department: Department name.
    """

    department: str = "Math"

