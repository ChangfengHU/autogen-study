# AutoGen Studio /api/runs 流程与 Agent 协作（对比 agentchat_fastapi）

本文梳理通过 curl 创建运行、以及随后触发多 Agent 协作（WebSocket）的完整链路，并与 `python/samples/agentchat_fastapi/app_agent.py` 的 `/chat` 接口做对比。

## 1) POST /api/runs/ 请求链路
- 入口：`autogenstudio/web/routes/runs.py#create_run`
  - 校验会话：从 DB 读取 `Session`（`session_id` + `user_id`）。
  - 新建 `Run`：状态 `created`，占位 `task`/`team_result`。
  - 返回：`{"run_id": <id>}`。
- 仅创建运行记录，不会直接启动 Agent。真正执行由前端随后发起的 WebSocket 消息触发。

示例（与你的请求等价）
- `POST /api/runs` body: `{"session_id": 8, "user_id": "guestuser@gmail.com"}`

## 2) WebSocket 启动与流式执行
- 入口：`autogenstudio/web/routes/ws.py#run_websocket`（路径 `/api/ws/runs/{run_id}`）
  - 建联：`WebSocketManager.connect()`（`web/managers/connection.py`）。
  - 等待客户端消息：
    - `type == "start"`：构造任务 `construct_task()`（`utils/utils.py`，支持文本+图片），调用 `ws_manager.start_stream(...)`。
- 执行核心：`WebSocketManager.start_stream()`
  - 读取并更新 `Run` 状态为 `active`；装载用户 `Settings` 中的 `environment`（作为 `env_vars`）。
  - 组装 `input_func`（用于运行时人机交互，消息经 WS 往返）。
  - 调用 `TeamManager.run_stream(...)`（`teammanager/teammanager.py`）：
    - `_create_team(...)`：将 `team_config`（JSON/YAML/ComponentModel）加载为 `BaseGroupChat`（`autogen_core`），必要时注入 env；为 `UserProxyAgent` 接管 `input_func`。
    - `team.run_stream(...)`：持续产出消息/事件（`autogen_agentchat.messages.*`、`LLMCallEvent` 等）。
  - `WebSocketManager`：
    - `_format_message(...)`：按类型映射为前端可消费的 JSON（message/message_chunk/result/completion）。
    - `_save_message(...)`：写入 DB（`Message` 表）。
    - 结束时 `complete/stop/error`，更新 `Run.team_result` 与状态。

数据模型（节选）：`autogenstudio/datamodel/db.py`
- `Session`、`Run(status, task, team_result)`、`Message(config, run_id, session_id)`，均为 SQLModel 表。

## 3) 与 samples/agentchat_fastapi 的对比
文件：`python/samples/agentchat_fastapi/app_agent.py`
- 相同点：
  - 都使用 `autogen_agentchat` 与 `autogen_core`（例如 `AssistantAgent`、`ChatCompletionClient`、消息模型 `TextMessage`）。
  - 模型客户端同源（`autogen_ext.models.*`），可经 YAML/env 加载。
- 不同点：
  - Studio：多 Agent/团队（`BaseGroupChat`）+ WebSocket 流式事件 + 数据库存储（会话/运行/消息/结果）+ 环境注入（用户 Settings）。
  - Sample：单接口 `/chat` 同步调用 `agent.on_messages(...)`，状态/历史用本地文件持久化，无团队编排/WS/DB。
  - 触发方式：Studio 先 `POST /api/runs`，再 WS `start` 带 `task` 与 `team_config`；Sample 直接 `POST /chat` 带入 `TextMessage`。
- 结论：两者共享相同底层 Agent/模型抽象，但 Studio 在其上增加了团队编排、会话化与流式管道。

## 4) 调试定位建议
- 创建运行：`web/routes/runs.py#create_run`
- 启动/消息流：`web/routes/ws.py#run_websocket` → `web/managers/connection.py#start_stream/_format_message/_save_message`
- 团队装配：`teammanager/teammanager.py#_create_team/run_stream`
- 任务构造：`utils/utils.py#construct_task`
- 数据库：`database/db_manager.py` + `datamodel/db.py`

***
如需进一步对照 UI 侧 `start` 载荷结构与前端处理，可结合 `frontend` 中的请求与 WS 消息格式。
