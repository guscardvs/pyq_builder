from typing import Callable, Tuple

from .base import FormatClause


class Select(FormatClause):
    def __init__(
        self,
        table: str,
        fields: Tuple[str, ...],
        stringify_statement: Callable[[str], str],
    ) -> None:
        self.table = table
        self.fields = fields
        self._stringify_statement = stringify_statement

    def stringify(self, string: str) -> str:
        return string.format(
            fields=", ".join(self._stringify_statement(field) for field in self.fields),
            table=self._stringify_statement(self.table),
        )
