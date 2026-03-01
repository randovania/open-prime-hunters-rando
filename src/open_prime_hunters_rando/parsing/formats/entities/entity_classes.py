from __future__ import annotations

import typing
from typing import TYPE_CHECKING, Literal, Protocol

if TYPE_CHECKING:
    from construct import Container


class CanHaveField(Protocol):
    _raw: Container


type FieldLocation = Literal["raw", "data", "header", "fields"]


class EntityField[T]:
    """
    Descriptor class to use to quickly define fields that take from `_raw`

    Example usage:
    ```
    class SomeEntity(Entity):
        our_field = EntityField[int]()
    ```
    """

    def __init__(
        self,
        location: FieldLocation | None = None,
    ):
        self.location = location

    def __set_name__(self, owner: type[CanHaveField], name: str) -> None:
        self.name = name

        if hasattr(owner, "_fields"):
            fields = typing.cast("dict[str, EntityField]", owner._fields)
            fields[name] = self

        if self.location is None:
            self.location = getattr(owner, "_default_field_location", "fields")

    def _data(self, obj: CanHaveField) -> Container:
        if self.location == "raw":
            return obj._raw
        if self.location == "data":
            return obj._raw.data
        if self.location == "header":
            return obj._raw.data.header
        if self.location == "fields":
            return obj._raw.data.fields

    def __get__(self, obj: CanHaveField | None, owner: type[CanHaveField] | None = None) -> T:
        if obj is None:
            raise AttributeError(
                f"Cannot access field '{self.name}' on class {owner} (must be accessed on an instance)"
            )
        return getattr(self._data(obj), self.name)

    def __set__(self, obj: CanHaveField, value: T) -> None:
        setattr(self._data(obj), self.name, value)


def field[T](
    type_hint: type[T],
    location: FieldLocation = "fields",
) -> EntityField[T]:
    return EntityField[T](location)
