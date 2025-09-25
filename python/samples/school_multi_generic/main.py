from __future__ import annotations

from .component import StudentConfig, TeacherConfig
from .student import Student
from .teacher import Teacher


def demo() -> None:
    alice = Student(name="Alice", config=StudentConfig(max_courses=2))
    bob = Teacher(name="Bob", config=TeacherConfig(department="Physics"))

    # Attendance
    alice.mark_present("2025-09-25")
    alice.mark_present("2025-09-26")
    bob.mark_present("2025-09-26")

    # Grading via teacher API (operates on student's GradebookMixin)
    bob.assign_grade(alice, "Math", 95)
    bob.assign_grade(alice, "Math", 85)
    bob.assign_grade(alice, "Chemistry", 88)

    print("== Attendance ==")
    print(f"Alice days: {alice.total_attendance()}  | Bob days: {bob.total_attendance()}")

    print("\n== Grades & Averages ==")
    for course in alice.courses():
        print(f"{course}: {alice.average(course):.1f}")

    print("\n== Enforce Student max_courses ==")
    try:
        bob.assign_grade(alice, "Biology", 90)  # exceeds max_courses=2
    except Exception as e:  # noqa: BLE001 demo output
        print("Adding Biology -> ERROR:", e)

    print("\n== Typed Configs ==")
    print("StudentConfig:", alice.config)
    print("TeacherConfig:", bob.config)

    print("\n== MRO (Student) ==")
    for cls in Student.mro():
        print(cls.__name__)

    print("\n== MRO (Teacher) ==")
        
    for cls in Teacher.mro():
        print(cls.__name__)


if __name__ == "__main__":
    demo()

