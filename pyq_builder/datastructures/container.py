from typing import Dict, Generic, TypeVar, cast

T = TypeVar("T")


class Container(Generic[T]):
    def __init__(self) -> None:
        self._container = cast(Dict[str, T], {})

    def __setitem__(self, name: str, contained: T):
        self._container[name] = contained

    def __getitem__(self, name: str) -> T:
        return self._container[name]
