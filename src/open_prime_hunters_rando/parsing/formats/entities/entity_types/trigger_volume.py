import enum
import typing

from construct import Construct, Flag, Int16sl, Int16ul, Int32sl, Int32ul, Padded, Struct

from open_prime_hunters_rando.parsing.common_types import MessageConstruct
from open_prime_hunters_rando.parsing.common_types.vectors import Vec3
from open_prime_hunters_rando.parsing.common_types.volume import (
    BaseVolumeType,
    BoxVolumeType,
    CollisionVolume,
    TriggerVolumeFlags,
    TriggerVolumeFlagsConstruct,
)
from open_prime_hunters_rando.parsing.construct_extensions import EnumAdapter
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType, Message


class TriggerVolumeType(enum.Enum):
    VOLUME = 0
    THRESHOLD = 1
    RELAY = 2
    AUTOMATIC = 3
    STATE_BITS = 4


TriggerVolumeEntityData = Struct(
    "subtype" / EnumAdapter(TriggerVolumeType, Int32ul),
    "volume" / CollisionVolume,
    "field3" / Int16ul,  # Unused
    "active" / Flag,
    "always_active" / Flag,
    "deactivate_after_use" / Padded(2, Flag),
    "repeat_delay" / Int16ul,
    "check_delay" / Int16ul,
    "required_state_bit" / Int16ul,
    "trigger_flags" / TriggerVolumeFlagsConstruct,
    "trigger_threshold" / Int32ul,
    "parent_id" / Padded(4, Int16sl),
    "parent_message" / MessageConstruct,
    "parent_message_param1" / Int32sl,
    "parent_message_param2" / Int32sl,
    "child_id" / Padded(4, Int16sl),
    "child_message" / MessageConstruct,
    "child_message_param1" / Int32sl,
    "child_message_param2" / Int32sl,
)


class TriggerVolume(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return TriggerVolumeEntityData

    subtype = field(TriggerVolumeType)

    volume = field(BaseVolumeType)

    field3 = field(int)

    active = field(bool)
    always_active = field(bool)
    deactivate_after_use = field(bool)

    repeat_delay = field(int)
    check_delay = field(int)

    required_state_bit = field(int)

    trigger_flags = field(TriggerVolumeFlags)

    trigger_threshold = field(int)

    parent_id = field(int)
    parent_message = field(Message)
    parent_message_param1 = field(int)
    parent_message_param2 = field(int)

    child_id = field(int)
    child_message = field(Message)
    child_message_param1 = field(int)
    child_message_param2 = field(int)

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.TRIGGER_VOLUME

    @classmethod
    def create(
        cls,
        node_name: str = "",
        layer_state: typing.Sequence[bool | int] = (False,) * 16,
        entity_id: int = -1,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 1.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 1.0),
        subtype: TriggerVolumeType = TriggerVolumeType.VOLUME,
        volume: BaseVolumeType | None = None,
        field3: int = 65535,
        active: bool = True,
        always_active: bool = True,
        deactivate_after_use: bool = True,
        repeat_delay: int = 0,
        check_delay: int = 0,
        required_state_bit: int = 0,
        trigger_flags: TriggerVolumeFlags = TriggerVolumeFlags.NONE,
        trigger_threshold: int = 0,
        parent_id: int = -1,
        parent_message: Message = Message.NONE,
        parent_message_param1: int = 0,
        parent_message_param2: int = 0,
        child_id: int = -1,
        child_message: Message = Message.NONE,
        child_message_param1: int = 0,
        child_message_param2: int = 0,
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
        obj.subtype = subtype
        obj.volume = volume
        obj.field3 = field3
        obj.active = active
        obj.always_active = always_active
        obj.deactivate_after_use = deactivate_after_use
        obj.repeat_delay = repeat_delay
        obj.check_delay = check_delay
        obj.required_state_bit = required_state_bit
        obj.trigger_flags = trigger_flags
        obj.trigger_threshold = trigger_threshold
        obj.parent_id = parent_id
        obj.parent_message = parent_message
        obj.parent_message_param1 = parent_message_param1
        obj.parent_message_param2 = parent_message_param2
        obj.child_id = child_id
        obj.child_message = child_message
        obj.child_message_param1 = child_message_param1
        obj.child_message_param2 = child_message_param2

        return obj
