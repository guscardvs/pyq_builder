import typing

T = typing.TypeVar("T")


class ResultParser:
    def __init__(self, result: typing.Union[dict, list]):
        self._result = result

    @property
    def _is_list(self):
        return isinstance(self._result, list)

    def get(self, target_class: typing.Type[T]) -> T:
        if self._is_list:
            raise NotImplementedError
        return target_class(self._result)

    def all(self, target_class: typing.Type[T]):
        if not self._is_list:
            return [self.get(target_class)]
        return [target_class(item) for item in self._result]
