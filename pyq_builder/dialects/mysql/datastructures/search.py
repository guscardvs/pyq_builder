import typing

from pyq_builder.dialects.mysql.utils import string_escape


class MysqlSearch:
    def __init__(self, fields: typing.Tuple[str, ...], table: str):
        self._fields = fields
        self._table = table

    def stringify(self):
        return "SELECT {} FROM {}".format(
            ", ".join(self._escape_field(field) for field in self._fields),
            string_escape(self._table),
        )

    def _escape_field(self, field: str):
        return f"{string_escape(self._table)}.{string_escape(field)}"
