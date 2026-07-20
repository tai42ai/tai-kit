# Contributing to tai42-kit

`tai42-kit` is generic leaf code: helpers, settings, pooled clients, and LLM/AI
factories. The hard rule (the leaf rule): **its only tai-* dependency is
`tai42-contract`** — it implements the contract's `BaseClient` Protocol and
consumes its manifest types; among tai-* packages it imports nothing else.

## Ground rules

- **Among tai-* packages, import `tai42_contract` only.** No other tai-* package:
  ```bash
  grep -rnE '(from|import)\s+tai_' src/ | grep -v tai42_contract   # only tai42_kit lines
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

## Dev

```bash
uv sync --extra dev --extra redis --extra curl --extra postgres
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest
```

For local cross-repo work, `make dev` editable-installs the sibling `tai-*`
checkouts this package builds on into the venv. While `[tool.uv.sources]` pins
those siblings to local paths, `uv sync` already installs them editable and
`make dev` changes nothing; once the lock resolves them from the registry,
`uv sync` / `uv run` installs the published builds instead, so re-run
`make dev` afterward to restore the editable links.

Before any commit, run a secret scan over `src/` and `tests/` (e.g.
`detect-secrets scan`).

## License

By contributing you agree your contributions are licensed under Apache-2.0.
