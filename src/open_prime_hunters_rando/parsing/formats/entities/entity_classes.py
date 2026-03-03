from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Literal

if TYPE_CHECKING:
    from construct import Container


class FieldsMixin:
    _raw: Container
    _fields: ClassVar[tuple[tuple[str, EntityField], ...]] = ()

    def __init_subclass__(cls, default_field_location: FieldLocation = "fields", **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

        for name, field in cls._fields:
            if field.location is None:
                field.location = default_field_location

    def __repr__(self) -> str:
        field_reprs = [f"{name}={getattr(self, name)}" for name, field in self.__class__._fields]
        return f"<{self.__class__.__name__} {' '.join(field_reprs)}>"

    def __str__(self) -> str:
        field_strs = [f"    {name} = {str(getattr(self, name))}" for name, field in self.__class__._fields]
        lines = [f"{self.__class__.__name__}:", *field_strs]
        return "\n".join(lines)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False

        for field_name, field in self.__class__._fields:
            if getattr(self, field_name, None) != getattr(other, field_name, None):
                return False

        return True


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

    def __set_name__(self, owner: type[FieldsMixin], name: str) -> None:
        self.name = name

        owner._fields += ((name, self),)

    def _data(self, obj: FieldsMixin) -> Container:
        if self.location == "raw":
            return obj._raw
        if self.location == "data":
            return obj._raw.data
        if self.location == "header":
            return obj._raw.data.header
        if self.location == "fields":
            return obj._raw.data.fields

    def __get__(self, obj: FieldsMixin | None, owner: type[FieldsMixin] | None = None) -> T:
        if obj is None:
            raise AttributeError(
                f"Cannot access field '{self.name}' on class {owner} (must be accessed on an instance)"
            )
        return getattr(self._data(obj), self.name)

    def __set__(self, obj: FieldsMixin, value: T) -> None:
        setattr(self._data(obj), self.name, value)

    def __repr__(self) -> str:
        return f"<{self.__class__} location='{self.location}'>"


def field[T](
    type_hint: type[T],
    location: FieldLocation | None = None,
) -> EntityField[T]:
    return EntityField[T](location)
