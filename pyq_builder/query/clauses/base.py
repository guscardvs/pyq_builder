from typing import Protocol


class Clause(Protocol):
    """Base Clause"""


class KeywordClause(Clause):
    def stringify(self) -> str:
        """Returns query as string"""


class FormatClause(Clause):
    def stringify(self, string: str) -> str:
        """Return query from parametrized string"""
