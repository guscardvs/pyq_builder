import typing

from pyq_builder import connection, datastructures, mapper
from pyq_builder.dialects.base import Dialect

from . import clauses

T = typing.TypeVar("T")


class Query(typing.Generic[T]):
    @typing.final
    def __init__(
        self,
        *,
        klass: typing.Type[T],
        table: typing.Optional[str] = None,
        mapper_class: typing.Type[mapper.Mapper[T]] = mapper.DataclassMapper,
        dialect: Dialect
    ) -> None:
        self._dialect = dialect
        self._mapper = mapper_class(klass, table)
        self._clauses = datastructures.RootNode[clauses.Clause, clauses.Clause]()
        self._post_init()

    def _post_init(self):
        """Post initialization hook"""

    @property
    def fields(self):
        return self._mapper.fields

    @property
    def fieldnames(self):
        return self._mapper.fieldnames

    @property
    def table(self):
        return self._mapper.table

    async def execute(self, conn: connection.Connection):
        await conn.execute(self._stringify(), self._acquire_params())

    def _stringify(self):
        pass

    def _acquire_params(self):
        pass

    def __str__(self) -> str:
        return self._stringify() or super().__str__()
