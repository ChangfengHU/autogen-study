# Chainlit 最小示例

本目录包含两个最小可运行的 Chainlit 示例：

1) 纯回声示例（不依赖任何大模型）
- 安装：
  - `pip install -U chainlit`
- 运行：
  - `chainlit run app.py -p 8002`
  - 浏览器打开提示的地址（通常 http://localhost:8002），输入任意文本，会原样回复。

2) OpenAI 直连示例（可选）
- 安装：
  - `pip install -U chainlit openai`
- 配置：
  - `export OPENAI_API_KEY=你的key`（Windows PowerShell: `$env:OPENAI_API_KEY="你的key"`）
- 运行：
  - `chainlit run app_openai.py -p 8003`

提示
- 若提示 `chainlit` 命令不存在，可用：`python -m chainlit run app.py`
- 端口被占用时，替换 `-p` 为其他端口（例如 8004）。

3) AutoGen AssistantAgent 示例（基于 autogen-agentchat）
- 安装：
  - `pip install -U chainlit autogen-agentchat "autogen-ext[openai]" pyyaml`
- 配置（任选其一）：
  - 用环境变量（推荐）：`export OPENAI_API_KEY=你的key`（可选 `OPENAI_MODEL=gpt-4o`）
  - 或编辑同目录/自定义路径的 `model_config.yaml`（可参考其他示例模板）
- 运行：
  - `chainlit run app_autogen_agent.py --port 8005`
  - 在页面输入消息，AssistantAgent 会调用所配置的模型生成回复。
