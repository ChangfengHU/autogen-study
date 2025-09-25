from __future__ import annotations

from typing import Dict, List, Set


class AttendanceMixin:
    """Reusable attendance behavior for persons."""

    def __init__(self) -> None:
        self._present_days: Set[str] = set()

    def mark_present(self, day: str) -> None:
        self._present_days.add(day)

    def total_attendance(self) -> int:
        return len(self._present_days)


class GradebookMixin:
    """Reusable gradebook behavior for learners.

    Expects an attribute ``config.max_courses`` when used with a typed component.
    """

    def __init__(self) -> None:
        self._grades: Dict[str, List[float]] = {}

    def record_grade(self, course: str, score: float) -> None:
        max_courses = getattr(self.config, "max_courses", 0)
        if course not in self._grades and max_courses > 0 and len(self._grades) >= max_courses:
            raise ValueError("Reached max_courses; cannot add a new course")
        self._grades.setdefault(course, []).append(score)

    def average(self, course: str) -> float:
        items = self._grades.get(course, [])
        if not items:
            return 0.0
        return sum(items) / len(items)

    def courses(self) -> List[str]:
        return list(self._grades.keys())

