# Contributing to tai42-kit

`tai42-kit` is generic leaf code: helpers, settings, pooled clients, and LLM/AI
factories. The hard rule (the leaf rule): **its only tai-* dependency is
`tai42-contract`** — it implements the contract's `BaseClient` Protocol and
consumes its manifest types; among tai-* packages it imports nothing else.

## Ground rules

- **Among tai-* packages, import `tai42_contract` only.** No other tai-* package:
  ```bash
  grep -rnE '(from|import)\s+tai(42)?_' src/ | grep -v tai42_contract   # only tai42_kit lines
  ```
- **Optional backends stay optional.** LLM providers, checkpoint/store backends,
  and pooled-client drivers (`redis` / `curl` / `postgres`) are
  `[project.optional-dependencies]`, imported lazily (providers/backends) or at
  the client submodule's top (drivers), so the core install stays lean.
- **Typed package** (`py.typed`). Pyright runs with 0 errors; a missing optional
  ML backend is a warning (not every dev installs torch).

## Layout

- `utils.data` — pure data/text transforms (json, json_schema, jq, mcp_output, string, url, yaml)
- `utils.lc` — LangChain / FastMCP / MCP glue (lc, signature)
- `utils.runtime` — IO/server/scheduling (files, schedule, uvicorn)
- `llm` — LLM/embedding factories, middleware, checkpoint/store, co-located `llm.settings`
- `clients` — pooled-client facade + engine + connection settings; drivers in `clients.impl`
- `net` — the SSRF url guard + the pinned `fetch_url` download (server-side URL fetches)
- `transport` — UDS MCP transports + `get_mcp_transport`
- `settings` — settings machinery (base + cache registry + self-registering schema registry); `logging` — logging settings + setup
- `plugins` — `tai-plugin.yml` spec loading: hardened YAML parsing + validation against the `tai42_contract.plugins.PluginSpec` schema

## Naming

PyPI is a flat namespace with no owner in the path, so distributions carry the
`tai42-` prefix. GitHub repositories keep their `tai-` names, because the
`tai42ai` organisation already namespaces them. Import packages follow the
distribution.

| Surface | Form |
| --- | --- |
| Distribution — PyPI, `pip install`, dependency pins | `tai42-<name>` |
| Import package | `tai42_<name>` |
| GitHub repository | `tai-<name>` |

So a dependency is declared as `tai42-<name>` while its repository is named
`tai-<name>`, and both spellings are correct in their own context.

Some surfaces are deliberately neither, and must not be renamed: the `tai` CLI
command (`tai42` is an alias), the Prometheus metric namespace (`tai_tool_*`),
`TAI_*` environment variables, and the `tai-plugin.yml` descriptor filename.

## Dev

```bash
uv venv --python 3.13
uv pip install --no-sources --editable ".[dev,llm,jq,uvicorn,redis,curl,postgres]"
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
uv run --no-sync pyright       # 0 errors; missing optional ML backends report as warnings
uv run --no-sync pytest --cov --cov-report=term-missing        # optional-extra tests skip if their extra is absent
```

`make dev` installs the sibling `tai-contract` repo as an editable install for local cross-repo development.

Before any commit, run a secret scan over `src/` and `tests/` (e.g.
`detect-secrets scan`).

## License

By contributing you agree your contributions are licensed under Apache-2.0.
