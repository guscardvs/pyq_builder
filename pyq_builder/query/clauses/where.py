import typing

from pyq_builder.dialects.base import Dialect
from pyq_builder.query import filters
from pyq_builder.query.clauses.base import KeywordClause
from pyq_builder.utils.params import Parameter

JoinsT = typing.TypeVar("JoinsT", bound=filters.FilterJoins)


class Where(KeywordClause):
    def __init__(
        self,
        field: Parameter,
        dialect: Dialect,
    ) -> None:
        self._field = field
        self._dialect = dialect

    def stringify(self) -> str:
        return str(self._field)

    def increment(self):
        return self, (self._field.position + 1)


class JoinsWhere(KeywordClause, typing.Generic[JoinsT]):
    def __init__(
        self,
        filterjoins: JoinsT,
        dialect: Dialect,
        outermost: bool = False,
    ):
        self._filterjoins = filterjoins
        self._dialect = dialect
        self._position = 0
        self._start = 0
        self._outermost = outermost

    def _parse_filter(self, filter_clause: filters.Filter, position: int):
        if isinstance(filter_clause, filters.Field):
            clause, self._position = Where(
                Parameter(
                    filter_clause.field,
                    self._dialect.stringify_statement(filter_clause.field),
                    self._dialect.resolver.compare(
                        filter_clause.field, filter_clause.comp
                    ),
                    position,
                ),
                self._dialect,
            ).increment()
            return clause
        if isinstance(filter_clause, filters.FilterJoins):
            return JoinsWhere(
                filter_clause,
                self._dialect,
            ).from_position(position)
        raise NotImplementedError

    @property
    def position(self):
        return self._position

    def from_position(self, position: int):
        self._position = self._start = position
        return self

    def iterate_all(self):
        for item in self._filterjoins.filters:
            if isinstance(item, type(self)):
                yield from item.iterate_all()
            yield item

    def iterate(self):
        for item in self._filterjoins.filters:
            self._position += 1
            yield item

    def increment(self):
        for item in self.iterate_all():
            self._position += 1
        return self

    def _comparator(
        self,
        filter_clause: filters.FilterJoins,
        where: typing.Iterable[typing.Union[Where, "JoinsWhere"]],
    ) -> str:
        def _invalid(arg):
            raise NotImplementedError

        _comparators = {
            filters.Or: self._dialect.resolver.or_,
            filters.And: self._dialect.resolver.and_,
            filters.FilterJoins: _invalid,
        }
        return _comparators[type(filter_clause)](where)

    def _resolve(self):
        for item in self.iterate():
            yield self._parse_filter(item, self._position)

    def stringify(self) -> str:
        self.from_position(self._start)
        if self._outermost:
            wrapper = lambda val: val
        else:
            wrapper = self._dialect.isolate
        return wrapper(self._comparator(self._filterjoins, self._resolve()))
