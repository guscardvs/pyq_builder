import typing

from pyq_builder.datastructures.comparison import Comparator, Comparison
from pyq_builder.datastructures.search import Search
from pyq_builder.dialects.base import HasStringify, Resolver
from pyq_builder.dialects.postgres.datastructures import comparator, search
from pyq_builder.dialects.postgres.dialect_filter import PostgresFilter


class PostgresResolver(Resolver):
    def or_(self, where: typing.Iterable[HasStringify]):
        return " OR ".join(item.stringify() for item in where)

    def and_(self, where: typing.Iterable[HasStringify]):
        return " AND ".join(item.stringify() for item in where)

    def compare(self, comp: Comparison, table: str) -> Comparator:
        return comparator.PostgresComparator(comp, table)

    def search(self, fields: typing.Tuple[str, ...], table: str) -> Search:
        return search.PostgresSearch(fields, table)

    def filter(self, resolved_fields: str) -> "PostgresFilter":
        return PostgresFilter(resolved_fields)
