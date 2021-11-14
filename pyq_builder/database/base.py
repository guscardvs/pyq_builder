import typing

from pyq_builder.config import QBuilderConfig
from pyq_builder.connection import Connection
from pyq_builder.database import pool

T = typing.TypeVar("T")


class Database:
    def __init__(
        self,
        *,
        uri: str = None,
        cfg: QBuilderConfig = None,
        pool_class: typing.Type[pool.Pool] = pool.DefaultPool
    ) -> None:
        """Receives database connection kwargs"""
        if not any((uri, cfg)):
            # TODO add custom exception
            raise Exception
        self._config = cfg or QBuilderConfig.from_uri(uri)
        self._connector = cfg.get_connector()
        self._pool = pool_class(cfg, self._connector)

    async def _create_pool(self) -> typing.Any:
        """Connects to database pool"""
        if self._pool.is_connected:
            # TODO add custom exception
            raise Exception
        await self._pool.create()

    async def acquire(self) -> typing.AsyncContextManager[Connection]:
        """Retrieves a connection from a pool"""
        async with self._pool.acquire() as conn:
            yield conn

    def is_closed(self, client: Connection):
        return self._connector.is_closed(client)

    async def close_client(self, client: Connection):
        await self._pool.release(client)
