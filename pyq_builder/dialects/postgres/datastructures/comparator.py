import pyq_builder.datastructures.comparison as cp
from pyq_builder.dialects.postgres.utils import string_escape

_comparison_mapping = {
    cp.Equal: "=",
    cp.NotEqual: "!=",
    cp.Greater: ">",
    cp.GreaterEqual: ">=",
    cp.Lesser: "<",
    cp.LesserEqual: "<=",
    cp.Like: "LIKE",
    cp.Contains: "IN",
    cp.Excludes: "NOT IN",
    cp.Is: "IS",
    cp.Comparison: "=",
}


class PostgresComparator(cp.Comparator):
    def __init__(self, comp: cp.Comparison, table: str):
        super().__init__(comp, table)
        self._comp = comp
        self._table = table

    def stringify(self, field: str, parameter: str) -> str:
        return " ".join([self._escape(field), self._resolve(), parameter])

    def _escape(self, field: str):
        return ".".join(
            item for item in (self._table and string_escape(self._table), field) if item
        )

    def _resolve(self):
        return _comparison_mapping[type(self._comp)]
