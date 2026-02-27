import enum

import construct
from construct import Byte, Int16sl, Int16ul, Int32sl, Int32ul, Struct, Vec3

from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_file import (
    EntityDataHeader,
    MessageConstruct,
    Vector3Fx,
)
from open_prime_hunters_rando.parsing.formats.entities.entity_types.volume_type import RawCollisionVolume, VolumeTypeCommon
from open_prime_hunters_rando.parsing.formats.entities.enum import Message


class ObjectFlags(enum.IntFlag):
    NONE = 0x0
    STATE_BIT0 = 0x1
    STATE_BIT1 = 0x2
    STATE = 0x3
    NO_ANIMATION = 0x4
    ENTITY_LINKED = 0x8
    IS_VISIBLE = 0x10


class ObjectEffectFlags(enum.IntFlag):
    NONE = 0x0
    USE_EFFECT_VOLUME = 0x1
    USE_EFFECT_OFFSET = 0x2
    REPEAT_SCAN_MESSAGE = 0x4
    WEAPON_ZOOM = 0x8
    ATTACH_EFFECT = 0x10
    DESTROY_EFFECT = 0x20
    ALWAYS_UPDATE_EFFECT = 0x40
    UNKNOWN = 0x8000


ObjectEntityData = Struct(
    "header" / EntityDataHeader,
    "flags" / construct.FlagsEnum(Byte, ObjectFlags),
    "_padding1" / Byte,
    "_padding2" / Int16ul,
    "effect_flags" / construct.FlagsEnum(Int32ul, ObjectEffectFlags),
    "model_id" / Int32sl,
    "linked_entity" / Int16sl,
    "scan_id" / Int16ul,
    "scan_message_target" / Int16sl,
    "_padding3" / Int16ul,
    "scan_message" / MessageConstruct,
    "effect_id" / Int32sl,
    "effect_interval" / Int32ul,
    "effect_on_inverals" / Int32ul,
    "effect_position_offset" / Vector3Fx,
    "volume" / RawCollisionVolume,
)


class Object(Entity):
    @classmethod
    def type_construct(cls) -> construct.Construct:
        return ObjectEntityData

    def flags(self, flag: ObjectFlags) -> bool:
        return self._raw.data.flags[flag.name]

    def set_flags(self, flag: ObjectFlags, state: bool) -> None:
        self._raw.data.flags[flag.name] = state

    def effect_flags(self, effect_flag: ObjectEffectFlags) -> bool:
        return self._raw.data.effect_flags[effect_flag.name]

    def set_effect_flags(self, effect_flag: ObjectEffectFlags, state: bool) -> None:
        self._raw.data.effect_flags[effect_flag.name] = state

    @property
    def model_id(self) -> int:
        return self._raw.data.model_id

    @model_id.setter
    def model_id(self, value: int) -> None:
        self._raw.data.model_id = value

    @property
    def linked_entity(self) -> int:
        return self._raw.data.linked_entity

    @linked_entity.setter
    def linked_entity(self, value: int) -> None:
        self._raw.data.linked_entity = value

    @property
    def scan_id(self) -> int:
        return self._raw.data.scan_id

    @scan_id.setter
    def scan_id(self, value: int) -> None:
        self._raw.data.scan_id = value

    @property
    def scan_message_target(self) -> int:
        return self._raw.data.scan_message_target

    @scan_message_target.setter
    def scan_message_target(self, value: int) -> None:
        self._raw.data.scan_message_target = value

    @property
    def scan_message(self) -> Message:
        return self._raw.data.scan_message

    @scan_message.setter
    def scan_message(self, value: Message) -> None:
        self._raw.data.scan_message = value

    @property
    def effect_id(self) -> int:
        return self._raw.data.effect_id

    @effect_id.setter
    def effect_id(self, value: int) -> None:
        self._raw.data.effect_id = value

    @property
    def effect_interval(self) -> int:
        return self._raw.data.effect_interval

    @effect_interval.setter
    def effect_interval(self, value: int) -> None:
        self._raw.data.effect_interval = value

    @property
    def effect_on_inverals(self) -> int:
        return self._raw.data.effect_on_inverals

    @effect_on_inverals.setter
    def effect_on_inverals(self, value: int) -> None:
        self._raw.data.effect_on_inverals = value

    @property
    def effect_position_offset(self) -> Vec3:
        return self._raw.data.effect_position_offset

    @effect_position_offset.setter
    def effect_position_offset(self, value: Vec3) -> None:
        self._raw.data.effect_position_offset = value

    def get_volume(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume)
