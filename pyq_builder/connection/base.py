import typing


class Connection(typing.Protocol):
    @property
    def closed(self) -> bool:
        return True

    async def read(self, q_str, params):
        pass

    async def write(self, q_str, params):
        pass

    async def close(self) -> None:
        """Closes DBAPI connection"""
