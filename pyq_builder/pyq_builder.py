import typing
from typing import Type, TypeVar

from pyq_builder.dialects.base import Compiler, Driver
from pyq_builder.query.main import Query

T = TypeVar("T")
R = TypeVar("R")


class QBuilder:
    def __init__(
        self,
        *,
        driver: Driver,
        compiler_class: typing.Type[Compiler] = Compiler,
    ) -> None:
        _compiler = compiler_class(driver.value)
        self._dialect = _compiler.get_dialect()

    def acquire_query(
        self, q_class: Type[Query[T]], *, klass: Type[T], **q_args
    ) -> Query[T]:
        q_args["klass"] = klass
        q_args.setdefault("dialect", self._dialect)
        return q_class(**q_args)

    @property
    def dialect(self):
        return self._dialect
