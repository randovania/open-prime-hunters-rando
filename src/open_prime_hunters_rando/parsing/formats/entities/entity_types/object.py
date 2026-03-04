import enum

import construct
from construct import Byte, Int16sl, Int16ul, Int32sl, Int32ul, Padded, Struct

from open_prime_hunters_rando.parsing.common_types import MessageConstruct
from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, CollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
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
    "flags" / Padded(4, construct.FlagsEnum(Byte, ObjectFlags)),
    "effect_flags" / construct.FlagsEnum(Int32ul, ObjectEffectFlags),
    "model_id" / Int32sl,
    "linked_entity" / Int16sl,
    "scan_id" / Int16ul,
    "scan_message_target" / Padded(4, Int16sl),
    "scan_message" / MessageConstruct,
    "effect_id" / Int32sl,
    "effect_interval" / Int32ul,
    "effect_on_inverals" / Int32ul,
    "effect_position_offset" / Vector3Fx,
    "volume" / CollisionVolume,
)


class Object(Entity):
    @classmethod
    def type_construct(cls) -> construct.Construct:
        return ObjectEntityData

    flags = field(dict[ObjectFlags, bool])

    effect_flags = field(dict[ObjectEffectFlags, bool])

    model_id = field(int)

    linked_entity = field(int)

    scan_id = field(int)
    scan_message_target = field(int)
    scan_message = field(Message)

    effect_id = field(int)
    effect_interval = field(int)
    effect_on_inverals = field(int)
    effect_position_offset = field(Vec3)

    volume = field(BaseVolumeType)
