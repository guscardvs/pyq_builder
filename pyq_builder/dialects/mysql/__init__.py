from . import clauses
from .dialect import MysqlDialect

MysqlDialect.register("where", clauses.WhereClauseParser())
MysqlDialect.register("select", clauses.SelectClauseParser())
