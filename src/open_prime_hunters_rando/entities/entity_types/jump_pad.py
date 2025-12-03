from construct import Container

from open_prime_hunters_rando.constants import Vec3
from open_prime_hunters_rando.entities.enum import TriggerVolumeFlags, VolumeType


class JumpPad:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def parent_id(self) -> int:
        return self._raw.parent_id

    @parent_id.setter
    def parent_id(self, value: int) -> None:
        self._raw.parent_id = value

    def get_volume(self) -> VolumeType:
        return VolumeType(self._raw.volume)

    @property
    def beam_vector(self) -> Vec3:
        return self._raw.beam_vector

    @beam_vector.setter
    def beam_vector(self, value: Vec3) -> None:
        self._raw.beam_vector = value

    @property
    def speed(self) -> float:
        return self._raw.speed

    @speed.setter
    def speed(self, value: float) -> None:
        self._raw.speed = value

    @property
    def control_lock_time(self) -> int:
        return self._raw.control_lock_time

    @control_lock_time.setter
    def control_lock_time(self, value: int) -> None:
        self._raw.control_lock_time = value

    @property
    def cooldown_time(self) -> int:
        return self._raw.cooldown_time

    @cooldown_time.setter
    def cooldown_time(self, value: int) -> None:
        self._raw.cooldown_time = value

    @property
    def active(self) -> bool:
        return self._raw.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.active = value

    @property
    def model_id(self) -> int:
        return self._raw.model_id

    @model_id.setter
    def model_id(self, value: int) -> None:
        self._raw.model_id = value

    @property
    def beam_type(self) -> int:
        return self._raw.beam_type

    @beam_type.setter
    def beam_type(self, value: int) -> None:
        self._raw.beam_type = value

    def trigger_flags(self, flag: TriggerVolumeFlags) -> bool:
        return self._raw.trigger_flags[flag.name]

    def set_trigger_flags(self, flag: TriggerVolumeFlags, state: bool) -> None:
        self._raw.trigger_flags[flag.name] = state
