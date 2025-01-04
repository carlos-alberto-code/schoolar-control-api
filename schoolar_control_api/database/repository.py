from typing import Type, TypeVar, List, Optional, Generic, Any

T = TypeVar("T")


class Repository(Generic[T]):
    def __init__(self, model: Type[T], session: Any):
        self._model = model
        self._session = session

    def get(self): ...
    def add(self): ...
    def update(self): ...
    def delete(self): ...
