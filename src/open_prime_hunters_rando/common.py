import math
from collections.abc import Iterator
from typing import IO, Any, SupportsIndex

import construct
from construct import Container, Enum, Int32ub


class EnumAdapter(construct.Adapter):
    def __init__(self, enum_class: Any, subcon: Any = Int32ub) -> None:
        super().__init__(Enum(subcon, enum_class))
        self._enum_class = enum_class

    def _decode(self, obj: str, context: Container, path: str) -> Enum | str:
        try:
            return self._enum_class[obj]
        except KeyError:
            return obj

    def _encode(self, obj: Enum, context: Container, path: str) -> str | Enum:
        if isinstance(obj, self._enum_class):
            return obj.name
        return obj


class FixedAdapter(construct.Adapter):
    """Fixed-point number with 12-bit fractional part"""

    def __init__(self) -> None:
        super().__init__(construct.Int32sl)

    def _decode(self, obj: int, context: dict, path: str) -> float:
        return float(obj) / 4096

    def _encode(self, obj: float, context: dict, path: str) -> int:
        return math.floor(obj * 4096)


class ColorRgbAdapter(construct.Adapter):
    """RGB for LightSource Entities"""

    def __init__(self) -> None:
        super().__init__(construct.Byte)

    def _decode(self, obj: int, context: dict, path: str) -> float:
        return float(obj) / 255

    def _encode(self, obj: float, context: dict, path: str) -> int:
        return math.floor(obj * 255)


class ErrorWithMessage(construct.Construct):
    def __init__(self, message: str, error: type[construct.ConstructError] = construct.ExplicitError) -> None:
        super().__init__()
        self.message = message
        self.flagbuildnone = True
        self.error = error

    def _parse(self, stream: IO[bytes], context: Any, path: str) -> None:
        message = construct.evaluate(self.message, context)
        raise self.error(f"Error field was activated during parsing with error {message}", path=path)

    def _build(self, obj: None, stream: IO[bytes], context: Any, path: str) -> int:
        message = construct.evaluate(self.message, context)
        raise self.error(f"Error field was activated during building with error {message}", path=path)

    def _sizeof(self, context: Container, path: str) -> int:
        raise construct.SizeofError("Error does not have size, because it interrupts parsing and building", path=path)


class Vec2:
    raw: list[float]

    def __init__(self, *args: float) -> None:
        self.raw = list(args)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Vec2):
            return self.raw == value.raw
        else:
            return self.raw == value

    def __iter__(self) -> Iterator[float]:
        return iter(self.raw)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({repr(self.raw)[1:-1]})"

    def __getitem__(self, key: SupportsIndex) -> float:
        return self.raw[key]

    def __setitem__(self, key: SupportsIndex, value: float) -> None:
        self.raw[key] = value

    @property
    def x(self) -> float:
        return self.raw[0]

    @x.setter
    def x(self, value: float) -> None:
        self.raw[0] = value

    @property
    def y(self) -> float:
        return self.raw[1]

    @y.setter
    def y(self, value: float) -> None:
        self.raw[1] = value


class Vec3(Vec2):
    @property
    def z(self) -> float:
        return self.raw[2]

    @z.setter
    def z(self, value: float) -> None:
        self.raw[2] = value

    @property
    def r(self) -> float:
        return self.x

    @r.setter
    def r(self, value: float) -> None:
        self.x = value

    @property
    def g(self) -> float:
        return self.y

    @g.setter
    def g(self, value: float) -> None:
        self.y = value

    @property
    def b(self) -> float:
        return self.z

    @b.setter
    def b(self, value: float) -> None:
        self.z = value


class Vec4(Vec3):
    @property
    def w(self) -> float:
        return self.raw[3]

    @w.setter
    def w(self, value: float) -> None:
        self.raw[3] = value

    @property
    def a(self) -> float:
        return self.w

    @a.setter
    def a(self, value: float) -> None:
        self.w = value
