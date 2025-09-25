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

    print("== 出勤情况 ==")
    print(f"Alice 天数: {alice.total_attendance()}  | Bob 天数: {bob.total_attendance()}")

    print("\n== 成绩与平均分 ==")
    for course in alice.courses():
        print(f"{course}: {alice.average(course):.1f}")

    print("\n== 验证学生 max_courses 限制 ==")
    try:
        bob.assign_grade(alice, "Biology", 90)  # exceeds max_courses=2
    except Exception as e:  # noqa: BLE001 demo output
        print("新增 Biology -> 错误:", e)

    print("\n== 强类型配置 ==")
    print("StudentConfig:", alice.config)
    print("TeacherConfig:", bob.config)

    print("\n== MRO（Student） ==")
    for cls in Student.mro():
        print(cls.__name__)

    print("\n== MRO（Teacher） ==")
        
    for cls in Teacher.mro():
        print(cls.__name__)


if __name__ == "__main__":
    demo()
