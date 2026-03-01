from construct import Construct, Flag, Int16ul, Int32sl, Int32ul, Padded, Struct

from open_prime_hunters_rando.parsing.common_types import FixedPoint
from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, RawCollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.trigger_volume import (
    TriggerVolumeFlags,
    TriggerVolumeFlagsConstruct,
)

JumpPadEntityData = Struct(
    "parent_id" / Int32sl,
    "_unused" / Int32ul,
    "volume" / RawCollisionVolume,
    "beam_vector" / Vector3Fx,
    "speed" / FixedPoint,
    "control_lock_time" / Int16ul,
    "cooldown_time" / Int16ul,
    "active" / Padded(4, Flag),
    "model_id" / Int32ul,
    "beam_type" / Int32ul,
    "trigger_flags" / TriggerVolumeFlagsConstruct,
)


class JumpPad(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return JumpPadEntityData

    parent_id = field(int)

    volume = field(BaseVolumeType)

    beam_vector = field(Vec3)

    speed = field(int)
    control_lock_time = field(int)
    cooldown_time = field(int)

    active = field(bool)

    model_id = field(int)
    beam_type = field(int)

    trigger_flags = field(dict[TriggerVolumeFlags, bool])
