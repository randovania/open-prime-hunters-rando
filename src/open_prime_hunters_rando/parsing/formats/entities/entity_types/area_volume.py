import typing

from construct import Byte, Construct, Flag, Int16sl, Int16ul, Int32sl, Int32ul, Padded, Struct

from open_prime_hunters_rando.parsing.common_types import MessageConstruct
from open_prime_hunters_rando.parsing.common_types.vectors import Vec3
from open_prime_hunters_rando.parsing.common_types.volume import (
    BaseVolumeType,
    BoxVolumeType,
    CollisionVolume,
)
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.trigger_volume import (
    TriggerVolumeFlags,
    TriggerVolumeFlagsConstruct,
)
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType, Message

AreaVolumeEntityData = Struct(
    "volume" / CollisionVolume,
    "field2" / Int16ul,  # Unused
    "active" / Flag,
    "always_active" / Flag,
    "allow_multiple" / Flag,
    "message_delay" / Byte,
    "field7" / Int16ul,  # Unused
    "inside_message" / MessageConstruct,
    "inside_message_param1" / Int32sl,
    "inside_message_param2" / Int32sl,
    "parent_id" / Padded(4, Int16sl),
    "exit_message" / MessageConstruct,
    "exit_message_param1" / Int32sl,
    "exit_message_param2" / Int32sl,
    "child_id" / Int16sl,
    "cooldown" / Int16ul,
    "priority" / Int32ul,
    "trigger_flags" / TriggerVolumeFlagsConstruct,
)


class AreaVolume(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return AreaVolumeEntityData

    volume = field(BaseVolumeType)

    field2 = field(int)

    active = field(bool)
    always_active = field(bool)
    allow_multiple = field(bool)

    message_delay = field(int)

    field7 = field(int)

    inside_message = field(Message)
    inside_message_param1 = field(int)
    inside_message_param2 = field(int)

    parent_id = field(int)

    exit_message = field(Message)
    exit_message_param1 = field(int)
    exit_message_param2 = field(int)

    child_id = field(int)

    cooldown = field(int)
    priority = field(int)

    trigger_flags = field(TriggerVolumeFlags)

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.AREA_VOLUME

    @classmethod
    def create(
        cls,
        node_name: str = "",
        layer_state: typing.Sequence[bool] = (False,) * 16,
        entity_id: int = -1,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 1.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 1.0),
        volume: BaseVolumeType | None = None,
        field2: int = 65535,
        active: bool = True,
        always_active: bool = True,
        allow_multiple: bool = True,
        message_delay: int = 0,
        field7: int = 0,
        inside_message: Message = Message.NONE,
        inside_message_param1: int = 0,
        inside_message_param2: int = 0,
        parent_id: int = -1,
        exit_message: Message = Message.NONE,
        exit_message_param1: int = 0,
        exit_message_param2: int = 0,
        child_id: int = -1,
        cooldown: int = 0,
        priority: int = 0,
        trigger_flags: TriggerVolumeFlags = TriggerVolumeFlags.NONE,
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
        obj.volume = volume
        obj.field2 = field2
        obj.active = active
        obj.always_active = always_active
        obj.allow_multiple = allow_multiple
        obj.message_delay = message_delay
        obj.field7 = field7
        obj.inside_message = inside_message
        obj.inside_message_param1 = inside_message_param1
        obj.inside_message_param2 = inside_message_param2
        obj.parent_id = parent_id
        obj.exit_message = exit_message
        obj.exit_message_param1 = exit_message_param1
        obj.exit_message_param2 = exit_message_param2
        obj.child_id = child_id
        obj.cooldown = cooldown
        obj.priority = priority
        obj.trigger_flags = trigger_flags

        return obj
