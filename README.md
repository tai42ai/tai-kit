# tai-kit

[![CI](https://github.com/tai42ai/tai-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/tai42ai/tai-kit/actions/workflows/ci.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

Generic leaf helpers, settings primitives, pooled clients, and LLM/AI factories
for the TAI ecosystem. It provides the reusable building blocks the server is
composed from: data and text transforms, LangChain/FastMCP/MCP tool glue, the
pooled-client facade and concrete drivers (`redis`, `curl`, `mcp`, `postgres`,
`http`), the SSRF URL guard and safe download, MCP client transports over a UDS
socket, the settings machinery, LLM/embedding factories with checkpoint/store
backends, and logging setup. Heavier backends are gated behind extras and
imported lazily. Typed package (`py.typed`).

## Position in the ecosystem

TAI is an open-source runtime for MCP tools, agents, and workflows — the server
that hosts a capability and supplies the operational layer around it (manifest
loading, access control, OAuth connectors, background execution, monitoring,
storage, and human-in-the-loop steps).

Three packages; each depends only on the ones to its left:

```
tai-contract  <--  tai-kit  <--  tai-skeleton
(interfaces)      (helpers)     (the server)
```

`tai-kit` obeys the leaf rule: its only tai-* dependency is `tai-contract`. It
implements the contract's `BaseClient` Protocol and consumes its manifest types;
among tai-* packages it depends on nothing else.

## Install

Requires **Python 3.13+**. Nothing is on PyPI yet, so install from source. Clone
this repo alongside `tai-contract` — this repo's `[tool.uv.sources]` points at
`../tai-contract` — then add it as an editable dependency of the environment
that runs the server:

```bash
git clone https://github.com/tai42ai/tai-contract
git clone https://github.com/tai42ai/tai-kit
cd tai-skeleton   # or your own app checkout
uv add --editable ../tai-kit   # once published: uv add tai-kit
```

Backends are gated behind extras, so install the ones you need — e.g. the
pooled-client drivers `tai-kit[redis]`, `tai-kit[postgres]`, `tai-kit[curl]`, the
checkpoint/store backends `tai-kit[langgraph-checkpoint-postgres]`,
`tai-kit[langgraph-checkpoint-sqlite]`, and LLM-provider backends like
`tai-kit[anthropic]`, `tai-kit[google]`, `tai-kit[mistral]`, `tai-kit[xai]`,
`tai-kit[ollama]`, `tai-kit[huggingface]`.

## Development

```bash
uv sync --extra dev --extra llm --extra jq --extra uvicorn --extra redis --extra curl --extra postgres
uv run ruff check .
uv run pyright       # 0 errors; missing optional ML backends are warnings
uv run pytest        # optional-extra tests skip if their extra is absent
```

See `CONTRIBUTING.md` for the rules.

## Documentation

The whole platform — concepts, guides, and the generated reference — lives in
the unified documentation site:

- Layering & the contract/kit/skeleton split: https://tai42.ai/concepts/layering
- Python SDK reference (this package's public API): https://tai42.ai/reference/python-sdk

## License

Apache-2.0. See `LICENSE` and `NOTICE`.
