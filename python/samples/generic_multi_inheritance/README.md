泛型 + 多继承（Python）

示例内容
- 多继承：将“对话上下文”与“泛型组件”两个基类的能力组合到一起。
- 泛型：通过 Component[TConfig] 提供强类型配置对象，便于静态检查与 IDE 补全。
- 实用模式：在保留领域上下文能力的同时，复用通用的组件基础设施。

文件结构
- component.py：泛型组件基类 Component[TConfig]。
- context_base.py：对话上下文基类 ChatCompletionContext（维护消息历史）。
- unbounded_context.py：多继承示例 UnboundedChatCompletionContext(ChatCompletionContext, Component[Config])。
- main.py：可运行的小示例。

这样写的好处
- 关注点分离：上下文负责对话历史；组件负责配置与生命周期。
- 类型安全：配置对象强类型（如 UnboundedChatCompletionContextConfig），提升 IDE 体验与类型检查质量。
- 可组合性：通过继承顺序（MRO）控制同名方法解析；一个对象同时具备上下文与组件能力。
- 复用性：可以基于相同的泛型组件基类创建更多上下文类型，只需换配置类型。

运行方式
1) 在仓库根目录，确保 Python 环境已激活（见仓库指南）。
2) 运行示例（使用模块方式确保包导入正常）：
   - python -m python.samples.generic_multi_inheritance.main

说明
- 示例尽量保持最小且带类型标注；更多提示参见代码中的中文注释与文档字符串。
