# AutoGen 项目架构图（高层）

```mermaid
flowchart LR
    subgraph UI[客户端与接口]
        direction TB
        PY[Python SDK<br/>autogen-agentchat]
        CLI[magentic-one-cli]
        STUDIO[AutoGen Studio 前端]
        DOTNET[.NET SDK]
    end

    subgraph CORE[核心与编排]
        direction TB
        AGC[AgentChat 核心：Agents/Teams/GroupChat]
        COND[条件/终止/任务]
        UIKIT[UI：Console/流式输出]
    end

    subgraph EXT[扩展与集成]
        direction TB
        MODELS[模型客户端：OpenAI/Azure/本地]
        TOOLS[工具与工作台：MCP/HTTP/搜索/自定义]
        SCHEMA[组件/Schema 生成]
    end

    subgraph SVC[服务与运行时（可选分布式）]
        direction TB
        GATE[Gateway / RPC / 事件桥]
        REG[Registry / 订阅与目录]
        ROUTE[Routing / 事件总线]
        STATE[AgentState / 持久化]
        WORKER[Agent Workers]
    end

    subgraph ECO[生态与支撑]
        direction TB
        BENCH[agbench 基准/评测]
        PROTO[Proto 定义 (gRPC/CloudEvents)]
        DOCS[文档/设计规范]
    end

    UI -->|调用| PY
    UI --> CLI
    UI --> STUDIO
    UI --> DOTNET

    PY --> AGC
    CLI --> AGC
    STUDIO --> AGC
    DOTNET --> GATE

    AGC <--> EXT
    AGC -->|事件/消息| GATE
    GATE <--> ROUTE
    ROUTE <--> REG
    ROUTE <--> STATE
    GATE <--> WORKER
    WORKER <--> AGC

    EXT --> MODELS
    EXT --> TOOLS
    EXT --> SCHEMA

    ECO --- BENCH
    ECO --- PROTO
    ECO --- DOCS

    classDef layer fill:#f9f9ff,stroke:#778,stroke-width:1px;
    classDef ext fill:#f8fff8,stroke:#787,stroke-width:1px;
    classDef svc fill:#fff8f8,stroke:#877,stroke-width:1px;
    class UI,CORE,ECO layer;
    class EXT ext;
    class SVC svc;
```

说明：
- UI 层包含 Python SDK、CLI、Studio 前端与 .NET 入口。
- 核心层（autogen-agentchat）提供多智能体、编排、条件/终止机制与基础 UI。
- 扩展层（autogen-ext）提供模型客户端与各类工具（含 MCP 工作台）。
- 服务层可在同进程内存总线或经 gRPC/事件总线分布式部署（Gateway/Registry/Routing/State/Worker）。
- 生态层含基准评测、Protobuf 定义与设计文档。

