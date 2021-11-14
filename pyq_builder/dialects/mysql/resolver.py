import typing

from pyq_builder.dialects.base import HasStringify, Resolver
from pyq_builder.dialects.mysql.comparator import MysqlComparator
from pyq_builder.utils.comparison import Comparison


class MysqlResolver(Resolver):
    def or_(self, where: typing.Iterable[HasStringify]):
        return " OR ".join((item.stringify() for item in where))

    def and_(self, where: typing.Iterable[HasStringify]):
        return " AND ".join((item.stringify() for item in where))

    def compare(self, field: str, comp: Comparison) -> MysqlComparator:
        return MysqlComparator(comp)
