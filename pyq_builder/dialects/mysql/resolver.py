import typing

from pyq_builder.datastructures.comparison import Comparison
from pyq_builder.dialects.base import HasStringify, Resolver
from pyq_builder.dialects.mysql.datastructures.comparator import \
    MysqlComparator
from pyq_builder.dialects.mysql.datastructures.search import MysqlSearch
from pyq_builder.dialects.mysql.dialect_filter import MysqlFilter


class MysqlResolver(Resolver):
    def or_(self, where: typing.Iterable[HasStringify]):
        return " OR ".join((item.stringify() for item in where))

    def and_(self, where: typing.Iterable[HasStringify]):
        return " AND ".join((item.stringify() for item in where))

    def compare(self, comp: Comparison, table: str) -> MysqlComparator:
        return MysqlComparator(comp, table)

    def search(self, fields: typing.Tuple[str], table: str) -> MysqlSearch:
        return MysqlSearch(fields, table)

    def filter(self, resolved_fields: str) -> MysqlFilter:
        return MysqlFilter(resolved_fields)
