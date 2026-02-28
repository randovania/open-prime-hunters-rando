from construct import Byte, Construct, Flag, Int16sl, Int16ul, Int32sl, Int32ul, Struct

from open_prime_hunters_rando.parsing.common_types.volume import (
    BaseVolumeType,
    CollisionVolume,
)
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_file import (
    MessageConstruct,
)
from open_prime_hunters_rando.parsing.formats.entities.entity_types.trigger_volume import (
    TriggerVolumeFlags,
    TriggerVolumeFlagsConstruct,
)
from open_prime_hunters_rando.parsing.formats.entities.enum import Message

AreaVolumeEntityData = Struct(
    "volume" / CollisionVolume,
    "_unused1" / Int16ul,
    "active" / Flag,
    "always_active" / Flag,
    "allow_mulitple" / Flag,
    "message_delay" / Byte,
    "_unused2" / Int16ul,
    "inside_message" / MessageConstruct,
    "inside_message_param1" / Int32sl,
    "inside_message_param2" / Int32sl,
    "parent_id" / Int16sl,
    "_padding3" / Int16ul,
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

    active = field(bool)
    always_active = field(bool)
    allow_mulitple = field(bool)

    message_delay = field(int)

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

    trigger_flags = field(dict[TriggerVolumeFlags, bool])
