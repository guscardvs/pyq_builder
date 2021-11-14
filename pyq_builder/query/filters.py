import typing
from dataclasses import dataclass

from typing_extensions import TypeGuard

from ..utils import comparison


class Filter:
    _mark: str = ""

    @property
    def mark(self):
        return self._mark

    def add_mark(self, mark: str):
        self._mark = mark
        return self


@dataclass
class Field(Filter):
    field: str
    comp: comparison.Comparison = comparison.Equal()

    def similar_to(self, filter_clause: Filter) -> "TypeGuard[Field]":
        if not isinstance(filter_clause, type(self)):
            return False
        return self.field == filter_clause.field


@dataclass(init=False, unsafe_hash=True)
class FilterJoins(Filter):
    filters: typing.Tuple[Filter, ...]

    def __init__(self, *filters: Filter) -> None:
        self.filters = filters

    def __bool__(self):
        return True


class Or(FilterJoins):
    pass


class And(FilterJoins):
    pass
