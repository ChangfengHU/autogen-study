# AutoGen 学习路线图

本路线图聚焦“先上手、再深入、最后扩展”。若需更详细的架构与流程分析，请参考仓库根目录的 `AutoGen_学习计划与架构分析.md`。

## 学习目标
- 理解 AutoGen 的核心抽象（Agent、Runtime、Message、Tools）。
- 能运行与改造多智能体示例，掌握工具调用与代码执行闭环。
- 具备针对业务场景进行扩展与集成的能力（自定义消息、内存、追踪等）。

## 阶段 0：准备环境（0.5 天）
- 克隆仓库并创建虚拟环境，安装依赖，配置 API Key。
- 通读 `README.md`，熟悉项目结构与主要目录（`autogen-core`、`autogen-agentchat`、`autogen-ext`、`python/samples`）。

## 阶段 1：核心概念速览（0.5–1 天）
- 阅读 `autogen-core` 的 Agent/Runtime/Message 关键接口，理解消息路由与生命周期。
- 关注 `BaseAgent` 与 `AgentRuntime` 的职责边界：注册、发送/发布消息、订阅主题、上下文管理。

## 阶段 2：AgentChat 进阶与工具使用（1–2 天）
- 阅读 `autogen-agentchat` 中的 `BaseChatAgent`、`AssistantAgent`、`UserProxyAgent`、`CodeExecutorAgent`。
- 重点把握工具调用流程：LLM 生成→工具执行→结果处理→反思/总结→多轮迭代（`max_tool_iterations`）。
- 跑通并改造一个“工具使用/代码执行”的最小闭环示例。

## 阶段 3：运行时与消息编排（1 天）
- 了解 `AgentRuntime` 的注册、路由（点对点、发布-订阅）与主题机制。
- 尝试实现一个包含移交（handoff）的小场景：一个 Agent 将任务移交给另一个 Agent。

## 阶段 4：样例与模式实践（1–2 天）
- 跑通 `python/samples` 与文档中的多智能体编排示例（如 GroupChat、Orchestration）。
- 引入 `workbench`（如 MCP）和 `memory`，观察对话上下文与工具结果如何被整合。

## 阶段 5：扩展与集成（持续）
- 自定义消息类型（参考 `autogen-core/models`）与序列化（`_serialization.py`）。
- 深入 `autogen-ext` 的模型与执行器集成方式，拓展到你的业务工具链。
- 加入追踪与可观测性，保证复杂多步流程的可调试性与可维护性。

## 快速上手建议
- 从最小可运行示例开始；每次只引入一个新概念。
- 多使用断点与日志，观察 Agent 与 Runtime 之间的消息流。
- 先模拟工具调用（本地函数），再接入真实外部系统。

## 参考资料
- 仓库根文档：`AutoGen_学习计划与架构分析.md`
- 官方文档：https://microsoft.github.io/autogen/

