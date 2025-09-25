学校示例：老师与学生（泛型 + 多继承）

场景
- 用多继承把可复用的行为（出勤、成绩册）组合到具体角色（学生、老师）。
- 用泛型保持角色配置的强类型，便于 IDE/mypy 静态检查。

文件
- component.py：泛型组件基类 Component[TConfig]；StudentConfig/TeacherConfig。
- mixins.py：AttendanceMixin（出勤）、GradebookMixin（成绩册，可复用横切能力）。
- base.py：PersonBase（公共属性 name）。
- student.py：Student(AttendanceMixin, GradebookMixin, Component[StudentConfig], PersonBase)。
- teacher.py：Teacher(AttendanceMixin, Component[TeacherConfig], PersonBase)，提供打分方法。
- main.py：可运行演示，包含出勤、打分、均分、MRO、强类型配置展示。

为什么这么设计
- 关注点分离：出勤/成绩做成 mixin 在多个角色间复用；人物、配置、行为解耦。
- 强类型配置（泛型）：`Component[StudentConfig]`/`Component[TeacherConfig]` 让配置具备静态校验与补全。
- 可组合性：通过多继承按 MRO 顺序叠加行为；若未来新增 `NotifyMixin`、`PersistMixin` 也能直接组合。

运行
- 在仓库根目录：
  - python -m python.samples.school_multi_generic.main
