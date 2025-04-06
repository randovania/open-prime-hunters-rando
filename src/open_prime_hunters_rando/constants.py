from __future__ import annotations

import construct
from construct import Adapter, Construct, Enum, Int32ub


def get_entity(entity_file: Construct, entity_id: int) -> int:
    entity_idx = 0
    for entity in entity_file.entities:
        if entity.size == 0:
            continue
        if entity.data.header.entity_id == entity_id:
            break
        entity_idx += 1
    return entity_idx


class EnumAdapter(Adapter):
    def __init__(self, enum_class, subcon=Int32ub):  # type:ignore
        super().__init__(Enum(subcon, enum_class))
        self._enum_class = enum_class

    def _decode(self, obj, context, path):  # type:ignore
        try:
            return self._enum_class[obj]
        except KeyError:
            return obj

    def _encode(self, obj, context, path):  # type:ignore
        if isinstance(obj, self._enum_class):
            return obj.name
        return obj


class ErrorWithMessage(Construct):
    def __init__(self, message, error=construct.ExplicitError) -> None:  # type:ignore
        super().__init__()
        self.message = message
        self.flagbuildnone = True
        self.error = error

    def _parse(self, stream, context, path) -> None:  # type:ignore
        message = construct.evaluate(self.message, context)
        raise self.error(f"Error field was activated during parsing with error {message}", path=path)

    def _build(self, obj, stream, context, path) -> None:  # type:ignore
        message = construct.evaluate(self.message, context)
        raise self.error(f"Error field was activated during building with error {message}", path=path)

    def _sizeof(self, context, path) -> None:  # type:ignore
        raise construct.SizeofError("Error does not have size, because it interrupts parsing and building", path=path)
