from pyq_builder.dialects.base import DialectFilter


class PostgresFilter(DialectFilter):
    def __init__(self, filters: str):
        self._filters = filters

    def stringify(self) -> str:
        return " ".join(("WHERE", self._filters))
