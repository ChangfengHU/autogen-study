from __future__ import annotations

from .base import PersonBase
from .component import Component, StudentConfig
from .mixins import AttendanceMixin, GradebookMixin


class Student(AttendanceMixin, GradebookMixin, Component[StudentConfig], PersonBase):
    """Student composed via multiple inheritance and typed config."""

    def __init__(self, name: str, config: StudentConfig) -> None:
        AttendanceMixin.__init__(self)
        GradebookMixin.__init__(self)
        Component.__init__(self, config)
        PersonBase.__init__(self, name)

