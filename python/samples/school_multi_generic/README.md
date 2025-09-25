School Example: Teacher & Student (Generics + Multiple Inheritance)

Scenario
- Use multiple inheritance to compose reusable behaviors (attendance, gradebook) into concrete roles (Student, Teacher).
- Use generics to keep role configuration strongly typed (better IDE/mypy support).

Files
- component.py: Generic Component[TConfig] base; StudentConfig/TeacherConfig.
- mixins.py: AttendanceMixin, GradebookMixin (可复用的横切功能)。
- base.py: PersonBase（公共属性：name）。
- student.py: Student(AttendanceMixin, GradebookMixin, Component[StudentConfig], PersonBase)。
- teacher.py: Teacher(AttendanceMixin, Component[TeacherConfig], PersonBase) + 评分方法。
- main.py: 可运行演示，包含出勤、打分、均分、MRO、强类型配置。

Why this design
- 分离关注点：出勤与成绩作为 mixin，可在不同角色间重用；人、配置、行为解耦。
- 强类型配置（泛型）：`Component[StudentConfig]`/`Component[TeacherConfig]` 让配置具备静态校验与补全。
- 可组合性：通过多继承按 MRO 顺序叠加行为；若未来新增 `NotifyMixin`、`PersistMixin` 可直接组合。

Run
- From repo root:
  - python -m python.samples.school_multi_generic.main

