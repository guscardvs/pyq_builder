from pyq_builder.dialects import base
from pyq_builder.dialects.postgres.resolver import PostgresResolver
from pyq_builder.dialects.postgres.utils import string_escape


class PostgresDialect(base.Dialect):

    resolver = PostgresResolver()

    @staticmethod
    def string_wrap(string: str) -> str:
        return f"'{string}'"

    @staticmethod
    def stringify_statement(string: str) -> str:
        return string_escape(string)

    @staticmethod
    def isolate(string) -> str:
        return f"({string})"
