import typing

from pyq_builder.datastructures.tree import Node

from . import clauses, filters
from .clauses import JoinsWhere
from .filters import And
from .main import Query

T = typing.TypeVar("T")


class Select(Query[T], typing.Generic[T]):
    def _post_init(self):
        self._core_node = typing.cast(
            Node[clauses.Select, clauses.Where],
            self._clauses.from_content(
                clauses.Select(self.table, self.fieldnames, self._dialect)
            ),
        )

    def where(self, *where: filters.Filter):
        for item in where:
            if isinstance(item, filters.Field) and item.table is None:
                item.table = self._core_node.content.table
        if len(where) == 1 and isinstance(where[0], filters.FilterJoins):
            clause = JoinsWhere(
                where[0],  # type: ignore
                self._dialect,
                outermost=True,
            )
        else:
            clause = JoinsWhere(
                And(*where),
                self._dialect,
                outermost=True,
            )
        self._core_node.from_content(clause)  # type: ignore
        return self

    def _stringify(self):
        where = self._core_node.children
        select_content = self._core_node.content.stringify()
        if not where:
            return select_content
        where_content = self._dialect.resolver.filter(
            ",".join(item.content.stringify() for item in where),
        ).stringify()
        return " ".join((select_content, where_content))
