import dataclasses
import typing

from pyq_builder import exc

from .base import AbstractBaseMapper, T


@dataclasses.dataclass
class Mock:
    name: str


class DataclassMapper(AbstractBaseMapper):
    def _validate_class(self, klass: typing.Type[T]) -> typing.Type[T]:
        if not dataclasses.is_dataclass(klass):
            raise exc.UnsupportedClass(
                "this class is not supported, use dataclass instead"
            )
        return klass

    def _post_init(self) -> None:
        self.fieldnames = tuple(self._klass.__dataclass_fields__.keys())
        self.fields = {
            key: val.type for key, val in self._klass.__dataclass_fields__.items()
        }

    def validate(self, field: str):
        if field not in self.fieldnames:
            raise AttributeError(f"query did not found field {field!r}")
