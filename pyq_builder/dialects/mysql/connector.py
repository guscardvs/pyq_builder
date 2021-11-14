import typing
from contextlib import asynccontextmanager

import aiomysql

from pyq_builder.config import QBuilderConfig
from pyq_builder.connection import Connection
from pyq_builder.utils.result import ResultParser


class MysqlConnection(Connection):
    def __init__(self, conn: aiomysql.Connection):
        self._db_conn = conn

    @property
    def closed(self) -> bool:
        return self._db_conn.closed

    async def close(self) -> None:
        if not self.closed:
            self._db_conn.close()

    def _parametrize(self, params: str):
        return

    def _parametrize_string(self, q_str: str):
        pass

    async def execute(self, q_str, params):
        async with self._db_conn.cursor() as cursor:
            executor = (
                cursor.execute if not isinstance(params, list) else cursor.executemany
            )
            result = await executor(
                self._parametrize_string(q_str), self._parametrize(params)
            )
            return ResultParser(result)


class MysqlConnector:
    _db_pool: typing.Optional[aiomysql.Pool]

    def __init__(self, cfg: QBuilderConfig):
        self._cfg = cfg
        self._db_pool = None

    @asynccontextmanager
    async def acquire(self) -> MysqlConnection:
        async with self._db_pool.acquire() as conn:
            yield MysqlConnection(conn)

    async def release(self, client: MysqlConnection) -> None:
        self._db_pool.release(client)

    @staticmethod
    def is_closed(client: MysqlConnection):
        return client.closed

    async def connect(self) -> MysqlConnection:
        """Should be used only by singleton pool"""
        return MysqlConnection(
            await aiomysql.connect(
                host=self._cfg.host,
                port=self._cfg.get_port(),
                user=self._cfg.user,
                password=self._cfg.passwd,
                db=self._cfg.name,
                cursorclass=aiomysql.DictCursor,
            )
        )

    async def create_pool(self):
        self._db_pool = aiomysql.create_pool(
            host=self._cfg.host,
            port=self._cfg.get_port(),
            user=self._cfg.user,
            password=self._cfg.passwd,
            db=self._cfg.name,
            maxsize=self._cfg.pool_size,
            pool_recycle=self._cfg.pool_recycle,
            cursorclass=aiomysql.DictCursor,
        )

    async def close_pool(self):
        self._db_pool.close()
        await self._db_pool.wait_closed()

    def is_connected(self):
        return self._db_pool is not None
