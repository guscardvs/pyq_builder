from pyq_builder.dialects.base import DialectParser


class WhereClauseParser(DialectParser):
    def stringify(self):
        return "WHERE"


class SelectClauseParser(DialectParser):
    def stringify(self):
        return "SELECT {fields} FROM {table}"
