from __future__ import annotations

from typing import Any

import construct
from construct import Adapter, Construct, Container, Enum, Int32ub


class EnumAdapter(Adapter):
    def __init__(self, enum_class: Any, subcon: Any = Int32ub) -> None:
        super().__init__(Enum(subcon, enum_class))
        self._enum_class = enum_class

    def _decode(self, obj: str, context: Container, path: str) -> Enum:
        try:
            return self._enum_class[obj]
        except KeyError:
            return obj

    def _encode(self, obj: Enum, context: Container, path: str) -> str:
        if isinstance(obj, self._enum_class):
            return obj.name
        return obj


class ErrorWithMessage(Construct):
    def __init__(self, message: str, error: type[construct.ConstructError] = construct.ExplicitError) -> None:
        super().__init__()
        self.message = message
        self.flagbuildnone = True
        self.error = error

    def _parse(self, stream: bytes, context: Container, path: str) -> None:
        message = construct.evaluate(self.message, context)
        raise self.error(f"Error field was activated during parsing with error {message}", path=path)

    def _build(self, obj: None, stream: bytes, context: Container, path: str) -> None:
        message = construct.evaluate(self.message, context)
        raise self.error(f"Error field was activated during building with error {message}", path=path)

    def _sizeof(self, context: Container, path: str) -> None:
        raise construct.SizeofError("Error does not have size, because it interrupts parsing and building", path=path)
