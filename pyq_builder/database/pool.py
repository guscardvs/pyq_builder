import typing
from contextlib import asynccontextmanager

from pyq_builder.config import QBuilderConfig
from pyq_builder.connection.base import Connection
from pyq_builder.dialects.base import Connector


class Pool(typing.Protocol):
    def __init__(self, config: QBuilderConfig, connector: Connector):
        ...

    @property
    def is_connected(self) -> bool:
        """Returns if pool is active"""
        return False

    async def create(self) -> None:
        """creates a pool inside itself"""

    @asynccontextmanager
    async def acquire(self) -> Connection:
        """returns a connectable"""

    async def release(self, client: Connection):
        """Releases a connection back to the pool"""

    async def close(self) -> None:
        """Closes inner pool"""


class SingletonPool:
    def __init__(self, config: QBuilderConfig, connector: Connector):
        self._config = config
        self._connector = connector

    _conn = None

    @property
    def conn(self):
        return type(self)._conn

    @property
    def is_connected(self):
        # TODO add implementation
        return self.conn is not None and self._connector.is_closed(self.conn)

    async def create(self):
        if self.conn is None:
            self._conn = await self._connector.connect()

    async def acquire(self):
        if not self.is_connected:
            await self.create()
        yield self.conn

    async def release(self, client: Connection):
        """Does nothing, just used by interface"""

    async def close(self):
        if self.is_connected:
            await self.conn.close()


class NullPool:
    def __init__(self, config: QBuilderConfig, connector: Connector):
        self._config = config
        self._connector = connector

    @staticmethod
    async def create():
        return None

    @property
    def is_connected(self):
        return False

    @asynccontextmanager
    async def acquire(self):
        yield None

    async def release(self, client: Connection):
        pass

    async def close(self):
        pass


class DefaultPool:
    def __init__(self, config: QBuilderConfig, connector: Connector):
        self._config = config
        self._connector = connector

    async def create(self):
        await self._connector.create_pool()

    @property
    def is_connected(self):
        return self._connector.is_connected

    @asynccontextmanager
    async def acquire(self):
        async with self._connector.acquire() as conn:
            yield conn

    async def release(self, client: Connection):
        await self._connector.release(client)

    async def close(self):
        await self._connector.close_pool()
