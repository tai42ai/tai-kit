"""tai-kit — generic leaf helpers, LLM factories, pooled clients, and settings
for the TAI ecosystem.

Utilities (data/runtime/langchain helpers), LLM provider + checkpoint/store
factories, pooled clients + MCP transports, and co-located pydantic-settings.
The only tai-* dependency is ``tai-contract`` (the leaf rule): kit implements its
``BaseClient`` Protocol and consumes its manifest types; it imports no other
tai-* package.

Deliberately light: nothing is re-exported here, so ``import tai_kit`` pulls no
vendor dependency (no langchain, no drivers). Import the subpackage you need —
each one (``tai_kit.llm``, ``tai_kit.clients``, ...) is the opt-in boundary for
its dependencies.
"""

from importlib.metadata import version

__version__ = version("tai-kit")

__all__ = ["__version__"]
