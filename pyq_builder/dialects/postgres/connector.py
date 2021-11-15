import typing
from contextlib import asynccontextmanager

import asyncpg

from pyq_builder.connection import Connection
from pyq_builder.datastructures.result import ResultParser
from pyq_builder.dialects.base import QBuilderConfig


class PostgresConnection(Connection):
    def __init__(self, conn: asyncpg.Connection):
        self._db_conn = conn

    @property
    def dialect_conn(self):
        return self._db_conn

    @property
    def closed(self) -> bool:
        return self._db_conn.is_closed()

    async def close(self) -> None:
        if not self.closed:
            await self._db_conn.close()

    def _parametrize(self, params: str):
        return

    def _parametrize_string(self, q_str: str):
        pass

    async def write(self, q_str, params):
        executor = (
            self._db_conn.execute
            if not isinstance(params, list)
            else self._db_conn.executemany
        )
        await executor(self._parametrize_string(q_str), self._parametrize(params))

    async def read(self, q_str, params):
        executor = (
            self._db_conn.fetchrow
            if not isinstance(params, list)
            else self._db_conn.fetch
        )
        result = await executor(
            self._parametrize_string(q_str), self._parametrize(params)
        )
        return ResultParser(result)


class PostgresConnector:
    _db_pool: typing.Optional[asyncpg.Pool]

    def __init__(self, cfg: QBuilderConfig):
        self._cfg = cfg
        self._db_pool = None

    @asynccontextmanager
    async def acquire(self) -> PostgresConnection:
        async with self._db_pool.acquire() as conn:
            async with conn.transaction():
                yield PostgresConnection(conn)

    async def release(self, client: PostgresConnection) -> None:
        await self._db_pool.release(client.dialect_conn)

    @staticmethod
    def is_closed(client: PostgresConnection):
        return client.closed

    async def connect(self) -> PostgresConnection:
        """Should be used only by singleton pool"""
        return PostgresConnection(
            await asyncpg.connect(
                host=self._cfg.host,
                port=self._cfg.get_port(),
                user=self._cfg.user,
                password=self._cfg.passwd,
                database=self._cfg.database,
            )
        )

    async def create_pool(self):
        self._db_pool = asyncpg.create_pool(
            host=self._cfg.host,
            port=self._cfg.get_port(),
            user=self._cfg.user,
            password=self._cfg.passwd,
            database=self._cfg.database,
            max_size=self._cfg.pool_size,
            max_inactive_connection_lifetime=self._cfg.pool_recycle,
        )

    async def close_pool(self):
        await self._db_pool.close()

    def is_connected(self):
        return self._db_pool is not None
