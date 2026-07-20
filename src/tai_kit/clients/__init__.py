"""Pooled clients + the generic client facade.

Each client subclasses ``PooledClient`` (per-loop pooling, satisfies the contract
``BaseClient`` Protocol) and is reached by class through ``client_ctx``. The
driver each impl needs is declared by an extra (``tai-kit[curl]`` /
``[postgres]``); import a driver submodule only when its driver is installed.
"""

from tai_contract.errors import ClientDisconnectedError

from tai_kit.clients.base import PooledClient, shutdown_all_clients
from tai_kit.clients.facade import client_ctx
from tai_kit.clients.settings import (
    ClientSettings,
    PostgresConnectionSettings,
    RedisConnectionSettings,
)

__all__ = [
    "ClientDisconnectedError",
    "ClientSettings",
    "PooledClient",
    "PostgresConnectionSettings",
    "RedisConnectionSettings",
    "client_ctx",
    "shutdown_all_clients",
]
