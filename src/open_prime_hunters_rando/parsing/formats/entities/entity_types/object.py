import typing

import construct
from construct import Byte, Int16sl, Int16ul, Int32sl, Int32ul, Padded, Struct

from open_prime_hunters_rando.parsing.common_types import BaseFlags, MessageConstruct
from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, BoxVolumeType, CollisionVolume
from open_prime_hunters_rando.parsing.construct_extensions import FlagsEnumAdapter
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType, Message


class ObjectFlags(BaseFlags):
    NONE = 0x0
    STATE_BIT0 = 0x1
    STATE_BIT1 = 0x2
    STATE = 0x3
    NO_ANIMATION = 0x4
    ENTITY_LINKED = 0x8
    IS_VISIBLE = 0x10


ObjectFlagsConstruct: FlagsEnumAdapter = FlagsEnumAdapter(ObjectFlags, Byte)


class ObjectEffectFlags(BaseFlags):
    NONE = 0x0
    USE_EFFECT_VOLUME = 0x1
    USE_EFFECT_OFFSET = 0x2
    REPEAT_SCAN_MESSAGE = 0x4
    WEAPON_ZOOM = 0x8
    ATTACH_EFFECT = 0x10
    DESTROY_EFFECT = 0x20
    ALWAYS_UPDATE_EFFECT = 0x40
    UNKNOWN = 0x8000


ObjectEffectFlagsConstruct: FlagsEnumAdapter = FlagsEnumAdapter(ObjectEffectFlags, Int32ul)

ObjectEntityData = Struct(
    "object_flags" / Padded(4, ObjectFlagsConstruct),
    "object_effect_flags" / ObjectEffectFlagsConstruct,
    "model_id" / Int32sl,
    "linked_entity_id" / Int16sl,
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

    object_flags = field(ObjectFlags)

    object_effect_flags = field(ObjectEffectFlags)

    model_id = field(int)

    linked_entity_id = field(int)

    scan_id = field(int)
    scan_message_target = field(int)
    scan_message = field(Message)

    effect_id = field(int)
    effect_interval = field(int)
    effect_on_inverals = field(int)
    effect_position_offset = field(Vec3)

    volume = field(BaseVolumeType)

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.OBJECT

    @classmethod
    def create(
        cls,
        node_name: str = "",
        layer_state: typing.Sequence[bool | int] = (False,) * 16,
        entity_id: int = -1,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 1.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 1.0),
        object_flags: ObjectFlags = ObjectFlags.NONE,
        object_effect_flags: ObjectEffectFlags = ObjectEffectFlags.NONE,
        model_id: int = -1,
        linked_entity_id: int = -1,
        scan_id: int = 0,
        scan_message_target: int = -1,
        scan_message: Message = Message.NONE,
        effect_id: int = 0,
        effect_interval: int = 0,
        effect_on_inverals: int = 0,
        effect_position_offset: Vec3 | tuple[float, float, float] = (0.0, 0.0, 1.0),
        volume: BaseVolumeType | None = None,
    ) -> typing.Self:
        if volume is None:
            volume = BoxVolumeType.create()

        obj = super().create(
            node_name,
            layer_state,
            entity_id,
            position,
            up_vector,
            facing_vector,
        )
        obj.object_flags = object_flags
        obj.object_effect_flags = object_effect_flags
        obj.model_id = model_id
        obj.linked_entity_id = linked_entity_id
        obj.scan_id = scan_id
        obj.scan_message_target = scan_message_target
        obj.scan_message = scan_message
        obj.effect_id = effect_id
        obj.effect_interval = effect_interval
        obj.effect_on_inverals = effect_on_inverals
        obj.effect_position_offset = Vec3(*effect_position_offset)
        obj.volume = volume

        return obj
