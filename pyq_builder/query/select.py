import typing

from pyq_builder.utils.tree import Node

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
                clauses.Select(
                    self.table, self.fieldnames, self._dialect.stringify_statement
                )
            ),
        )

    def where(self, *where: filters.Filter):
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
        select_content = self._core_node.content.stringify(
            self._dialect["select"].stringify(),
        )
        if not where:
            return select_content
        where_content = "{} {}".format(
            self._dialect["where"].stringify(),
            ",".join(item.content.stringify() for item in where),
        )
        return " ".join((select_content, where_content))
