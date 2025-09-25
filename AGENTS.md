# Repository Guidelines

This repository hosts AutoGen across Python, .NET, and a small web UI. Follow these concise conventions to keep contributions consistent and easy to review.

## Project Structure & Module Organization
- `python/`: `uv` workspace with packages in `python/packages/*` (e.g., `autogen-core`, `autogen-agentchat`, `autogen-ext`, `autogen-studio`); tests live per package under `tests/`; examples under `python/samples/`; docs in `python/docs/`.
- `dotnet/`: C# solution (`dotnet/AutoGen.sln`) with `src/` and `test/` projects.
- `protos/`: Shared `.proto` files.
- `docs/`: Top-level docs/design notes.
- Studio frontend: `python/packages/autogen-studio/frontend/` (Gatsby/TypeScript).

## Build, Test, and Development Commands
Python (run from `python/`):
- Setup: `uv sync --all-extras && source .venv/bin/activate`
- All checks: `poe check`
- Format/Lint/Types/Tests: `poe format` | `poe lint` | `poe mypy` | `poe pyright` | `poe test`
- Docs: `poe docs-build` | `poe docs-serve`
- Protobuf: `poe gen-proto`

.NET (from repo root or `dotnet/`):
- Build: `dotnet build dotnet/AutoGen.sln -c Release`
- Test: `dotnet test dotnet/AutoGen.sln -c Release`

Studio UI (optional):
- `cd python/packages/autogen-studio/frontend && npm ci && npm run build`

## Coding Style & Naming Conventions
- Python: Format with Ruff (line length 120); lint with Ruff; strict type checks via MyPy/Pyright; Google-style docstrings; prefer `pytest` (avoid `unittest`).
- C#: Respect repo `.editorconfig`; PascalCase for types/members, camelCase for locals/params; enable nullable and treat warnings seriously.

## Testing Guidelines
- Python: Place tests under `<pkg>/tests/` as `test_*.py`; use fixtures/mocks; skip external tests if env vars are missing; run subsets via `pytest -k` or markers (e.g., `-m grpc`).
- .NET: xUnit-based tests in `dotnet/test`; some require API keys (e.g., `OPENAI_API_KEY`) and will auto-skip if unset.

## Commit & Pull Request Guidelines
- Use Conventional Commits: `type(scope): subject` (e.g., `feat(agentchat): add tool handoffs`).
- PRs: clear description, linked issues, tests/docs as needed; pass `poe check` (Python) and `dotnet build/test`; add screenshots for Studio UI changes.

## Security & Configuration Tips
- Never commit secrets. Provide keys via environment variables (e.g., `OPENAI_API_KEY`); use a local `.env` that is not checked in.
- When changing `protos/`, regenerate Python stubs with `poe gen-proto` and update affected packages/tests.

