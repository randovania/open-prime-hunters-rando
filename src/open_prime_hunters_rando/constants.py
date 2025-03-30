from __future__ import annotations

import construct
from construct import Adapter, Construct, Enum, Int32ub

ITEM_TYPES_TO_IDS = {
    "HealthMedium": 0,
    "HealthSmall": 1,
    "HealthBig": 2,
    "EnergyTank": 4,
    "VoltDriver": 5,
    "MissileExpansion": 6,
    "Battlehammer": 7,
    "Imperialist": 8,
    "Judicator": 9,
    "Magmaul": 10,
    "ShockCoil": 11,
    "OmegaCannon": 12,
    "UASmall": 13,
    "UABig": 14,
    "MissileSmall": 15,
    "MissileBig": 16,
    "UAExpansion": 18,
    "ArtifactKey": 19,
}


def get_entity(entity_file: Construct, entity_id: int) -> int:
    entity_idx = 0
    for entity in entity_file.entities:
        if entity.length == 0:
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
