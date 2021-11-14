import pyq_builder.utils.comparison as cp

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


class MysqlComparator(cp.Comparator):
    def __init__(self, comp: cp.Comparison):
        super().__init__(comp)
        self._comp = comp

    def stringify(self, field: str, parameter: str) -> str:
        return " ".join([field, self._resolve(), parameter])

    def _resolve(self):
        return _comparison_mapping[type(self._comp)]
