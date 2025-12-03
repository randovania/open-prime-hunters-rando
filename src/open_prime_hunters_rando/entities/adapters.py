import math
from typing import IO, Any

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
