from psycopg import AsyncConnection
from psycopg.rows import TupleRow
from psycopg.types.json import Json
from psycopg_pool import AsyncConnectionPool

from tai_kit.clients.base import PooledClient, reject_unknown_connection_kwargs

# ``Json`` is re-exported so callers wrap jsonb params through the pooled
# client's own module rather than importing psycopg directly — every pg
# primitive the app touches is reached through the kit client layer.
__all__ = ["Json", "PostgresClient"]

# The pool's default connection type. Naming it lets the pooled-client generic
# resolve concretely (the AsyncConnectionPool default hides ACT behind a cast).
_Pool = AsyncConnectionPool[AsyncConnection[TupleRow]]

# Connection kwargs a Postgres client accepts — the identity produced by
# ``PostgresConnectionSettings.client_kwargs``. Anything else is rejected so it
# can't silently split the pool key.
_ALLOWED_KWARGS = frozenset({"dsn", "min_size", "max_size"})


class PostgresClient(PooledClient[_Pool]):
    """Pooled ``psycopg_pool.AsyncConnectionPool``, one pool per (DSN, size) per
    loop. Compose ``PostgresConnectionSettings`` for the connection kwargs."""

    async def _create(self, **kwargs) -> _Pool:
        if "dsn" not in kwargs:
            raise KeyError("Postgres client requires a 'dsn' kwarg")
        dsn = kwargs["dsn"]
        if not dsn or not isinstance(dsn, str):
            raise ValueError("Postgres client 'dsn' must be a non-empty string")
        reject_unknown_connection_kwargs("Postgres client", kwargs, _ALLOWED_KWARGS)

        pool = AsyncConnectionPool(
            conninfo=dsn,
            min_size=kwargs.get("min_size", 2),
            max_size=kwargs.get("max_size", 10),
            open=False,
            connection_class=AsyncConnection,
        )
        await pool.open()
        return pool

    async def _close(self, client: _Pool):
        await client.close()

    def _disconnection_exceptions(self) -> tuple[type[Exception], ...]:
        import psycopg

        return (psycopg.OperationalError,)
