from construct import Byte, Construct, Flag, Int16ul, Int32sl, Int32ul, Struct

from open_prime_hunters_rando.common import FixedPoint, Vec3
from open_prime_hunters_rando.entities.entity import Entity
from open_prime_hunters_rando.entities.entity_file import (
    EntityDataHeader,
    Vector3Fx,
)
from open_prime_hunters_rando.entities.entity_types.trigger_volume import (
    TriggerVolumeFlags,
    TriggerVolumeFlagsConstruct,
)
from open_prime_hunters_rando.entities.entity_types.volume_type import RawCollisionVolume
from open_prime_hunters_rando.entities.enum import VolumeTypeCommon

JumpPadEntityData = Struct(
    "header" / EntityDataHeader,
    "parent_id" / Int32sl,
    "_unused" / Int32ul,
    "volume" / RawCollisionVolume,
    "beam_vector" / Vector3Fx,
    "speed" / FixedPoint,
    "control_lock_time" / Int16ul,
    "cooldown_time" / Int16ul,
    "active" / Flag,
    "_padding1" / Byte,
    "_padding2" / Int16ul,
    "model_id" / Int32ul,
    "beam_type" / Int32ul,
    "trigger_flags" / TriggerVolumeFlagsConstruct,
)


class JumpPad(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return JumpPadEntityData

    @property
    def parent_id(self) -> int:
        return self._raw.data.parent_id

    @parent_id.setter
    def parent_id(self, value: int) -> None:
        self._raw.data.parent_id = value

    def get_volume(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume)

    @property
    def beam_vector(self) -> Vec3:
        return self._raw.data.beam_vector

    @beam_vector.setter
    def beam_vector(self, value: Vec3) -> None:
        self._raw.data.beam_vector = value

    @property
    def speed(self) -> float:
        return self._raw.data.speed

    @speed.setter
    def speed(self, value: float) -> None:
        self._raw.data.speed = value

    @property
    def control_lock_time(self) -> int:
        return self._raw.data.control_lock_time

    @control_lock_time.setter
    def control_lock_time(self, value: int) -> None:
        self._raw.data.control_lock_time = value

    @property
    def cooldown_time(self) -> int:
        return self._raw.data.cooldown_time

    @cooldown_time.setter
    def cooldown_time(self, value: int) -> None:
        self._raw.data.cooldown_time = value

    @property
    def active(self) -> bool:
        return self._raw.data.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.data.active = value

    @property
    def model_id(self) -> int:
        return self._raw.data.model_id

    @model_id.setter
    def model_id(self, value: int) -> None:
        self._raw.data.model_id = value

    @property
    def beam_type(self) -> int:
        return self._raw.data.beam_type

    @beam_type.setter
    def beam_type(self, value: int) -> None:
        self._raw.data.beam_type = value

    def trigger_flags(self, flag: TriggerVolumeFlags) -> bool:
        return self._raw.data.trigger_flags[flag.name]

    def set_trigger_flags(self, flag: TriggerVolumeFlags, state: bool) -> None:
        self._raw.data.trigger_flags[flag.name] = state
