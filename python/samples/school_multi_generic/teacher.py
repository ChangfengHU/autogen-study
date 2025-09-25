from __future__ import annotations

from .base import PersonBase
from .component import Component, TeacherConfig
from .mixins import AttendanceMixin, GradebookMixin


class Teacher(AttendanceMixin, Component[TeacherConfig], PersonBase):
    """具备出勤与强类型配置的教师类。

    提供对具备成绩册能力（GradebookMixin）的对象进行打分的操作。
    """

    def __init__(self, name: str, config: TeacherConfig) -> None:
        # 显式初始化各父类，清晰展示组合关系
        AttendanceMixin.__init__(self)
        Component.__init__(self, config)
        PersonBase.__init__(self, name)

    def assign_grade(self, learner: GradebookMixin, course: str, score: float) -> None:
        # 对具备成绩册能力的对象进行打分
        learner.record_grade(course, score)
