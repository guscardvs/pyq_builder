import abc
from typing import Protocol


class Comparison(abc.ABC):
    pass


class Equal(Comparison):
    pass


class NotEqual(Comparison):
    pass


class Greater(Comparison):
    pass


class GreaterEqual(Comparison):
    pass


class Lesser(Comparison):
    pass


class LesserEqual(Comparison):
    pass


class Like(Comparison):
    pass


class Contains(Comparison):
    pass


class Excludes(Comparison):
    pass


class Is(Comparison):
    pass


class Comparator(Protocol):
    def __init__(self, comp: Comparison, table: str):
        self._comp = comp
        self._table = table

    @property
    def table(self):
        return self._table

    def stringify(self, field: str, parameter: str) -> str:
        ...
