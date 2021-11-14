import typing


class Connection(typing.Protocol):
    @property
    def closed(self) -> bool:
        return True

    async def execute(self, q_str, params):
        pass

    async def close(self) -> None:
        """Closes DBAPI connection"""
