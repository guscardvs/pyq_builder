import abc
import typing

T = typing.TypeVar("T")


class Mapper(typing.Protocol[T]):
    fieldnames: typing.Tuple[str, ...]
    fields: typing.Dict[str, type]
    table: str
    _klass: typing.Type[T]

    @abc.abstractmethod
    def __init__(
        self, klass: typing.Type[T], table: typing.Optional[str] = None
    ) -> None:
        ...

    def _validate_class(self, klass: typing.Type[T]) -> typing.Type[T]:
        """Validates klass received or raises Unsupported class Exception"""

    def _post_init(self) -> None:
        """Post init required hook"""

    def validate(self, field: str):
        """Raise exception if field is not contained in fieldnames"""


class AbstractBaseMapper(Mapper[T]):
    """Base Concrete implementation of Query Protocol"""

    def __init__(
        self, klass: typing.Type[T], table: typing.Optional[str] = None
    ) -> None:
        self._klass = self._validate_class(klass)
        self.table = table or klass.__name__.lower()
        self._post_init()

    @abc.abstractmethod
    def _post_init(self) -> None:
        """Post init required hook"""

    @abc.abstractmethod
    def _validate_class(self, klass: typing.Type[T]) -> typing.Type[T]:
        """Validates klass received or raises Unsupported class Exception"""
