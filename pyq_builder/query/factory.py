from typing import Generic, Type, TypeVar

from pyq_builder.dialects.base import Dialect

from .main import Query

T = TypeVar("T", bound=Query)
R = TypeVar("R")


class Executable(Generic[T, R]):
    def __init__(self, q_class: Type[T], **q_args) -> None:
        self._q_class = q_class
        self._q_args = q_args

    def get(self, dialect: Dialect) -> T:
        self._q_args.setdefault("dialect", dialect)
        return self._q_class[R](**self._q_args)


class Factory(Generic[T]):
    def __init__(self, q_class: Type[T]) -> None:
        self._q_class = q_class

    def __call__(self, klass: Type[R], **q_args) -> Executable[T, R]:
        return Executable(self._q_class, klass=klass, **q_args)
