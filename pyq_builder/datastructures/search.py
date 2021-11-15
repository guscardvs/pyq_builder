import abc
import typing


class Search(typing.Protocol):
    @abc.abstractmethod
    def __init__(
        self,
        fields: typing.Tuple[str, ...],
        table: str,
    ):
        ...

    def stringify(self) -> str:
        ...
