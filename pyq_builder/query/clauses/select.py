from typing import Tuple

from pyq_builder.dialects.base import Dialect

from .base import KeywordClause


class Select(KeywordClause):
    def __init__(self, table: str, fields: Tuple[str, ...], dialect: Dialect) -> None:
        self._table = table
        self._fields = fields
        self._dialect = dialect

    @property
    def table(self):
        return self._table

    def stringify(self) -> str:
        return self._dialect.resolver.search(self._fields, self._table).stringify()
