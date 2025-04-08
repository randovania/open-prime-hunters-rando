from __future__ import annotations

import construct
from construct import Adapter, Construct, Enum, Int32ub


class EnumAdapter(Adapter):
    def __init__(self, enum_class, subcon=Int32ub):
        super().__init__(Enum(subcon, enum_class))
        self._enum_class = enum_class

    def _decode(self, obj, context, path):
        try:
            return self._enum_class[obj]
        except KeyError:
            return obj

    def _encode(self, obj, context, path):
        if isinstance(obj, self._enum_class):
            return obj.name
        return obj


class ErrorWithMessage(Construct):
    def __init__(self, message, error=construct.ExplicitError) -> None:
        super().__init__()
        self.message = message
        self.flagbuildnone = True
        self.error = error

    def _parse(self, stream, context, path):
        message = construct.evaluate(self.message, context)
        raise self.error(f"Error field was activated during parsing with error {message}", path=path)

    def _build(self, obj, stream, context, path):
        message = construct.evaluate(self.message, context)
        raise self.error(f"Error field was activated during building with error {message}", path=path)

    def _sizeof(self, context, path):
        raise construct.SizeofError("Error does not have size, because it interrupts parsing and building", path=path)
