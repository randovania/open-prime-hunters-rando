import enum

from construct import Construct, Flag, Int16sl, Int16ul, Int32sl, Int32ul, Padded, Struct

from open_prime_hunters_rando.parsing.common_types import MessageConstruct
from open_prime_hunters_rando.parsing.common_types.volume import (
    BaseVolumeType,
    RawCollisionVolume,
    TriggerVolumeFlags,
    TriggerVolumeFlagsConstruct,
)
from open_prime_hunters_rando.parsing.construct_extensions import EnumAdapter
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.enum import Message


class TriggerVolumeType(enum.Enum):
    VOLUME = 0
    THRESHOLD = 1
    RELAY = 2
    AUTOMATIC = 3
    STATE_BITS = 4


TriggerVolumeEntityData = Struct(
    "subtype" / EnumAdapter(TriggerVolumeType, Int32ul),
    "volume" / RawCollisionVolume,
    "_unused" / Int16ul,
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

    active = field(bool)
    always_active = field(bool)
    deactivate_after_use = field(bool)

    repeat_delay = field(int)
    check_delay = field(int)

    required_state_bit = field(int)

    trigger_flags = field(dict[TriggerVolumeFlags, bool])

    trigger_threshold = field(int)

    parent_id = field(int)
    parent_message = field(Message)
    parent_message_param1 = field(int)
    parent_message_param2 = field(int)

    child_id = field(int)
    child_message = field(Message)
    child_message_param1 = field(int)
    child_message_param2 = field(int)
