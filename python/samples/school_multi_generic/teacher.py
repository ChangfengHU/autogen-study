from __future__ import annotations

from .base import PersonBase
from .component import Component, TeacherConfig
from .mixins import AttendanceMixin, GradebookMixin


class Teacher(AttendanceMixin, Component[TeacherConfig], PersonBase):
    """Teacher with attendance and typed config.

    Provides an operation to assign a grade to any object supporting Gradebook-like API.
    """

    def __init__(self, name: str, config: TeacherConfig) -> None:
        AttendanceMixin.__init__(self)
        Component.__init__(self, config)
        PersonBase.__init__(self, name)

    def assign_grade(self, learner: GradebookMixin, course: str, score: float) -> None:
        learner.record_grade(course, score)

