from pyq_builder.dialects.base import Dialect
from pyq_builder.dialects.mysql.resolver import MysqlResolver


class MysqlDialect(Dialect):
    resolver = MysqlResolver()

    @staticmethod
    def string_wrap(string: str):
        return f"{string!r}"

    @staticmethod
    def stringify_statement(string: str) -> str:
        return f"`{string}`"

    @staticmethod
    def isolate(string) -> str:
        return f"({string})"
