from construct import Container

from open_prime_hunters_rando.common import Vec3
from open_prime_hunters_rando.entities.enum import Message, ObjectEffectFlags, ObjectFlags, VolumeType


class Object:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def flags(self, flag: ObjectFlags) -> bool:
        return self._raw.flags[flag.name]

    def set_flags(self, flag: ObjectFlags, state: bool) -> None:
        self._raw.flags[flag.name] = state

    def effect_flags(self, effect_flag: ObjectEffectFlags) -> bool:
        return self._raw.effect_flags[effect_flag.name]

    def set_effect_flags(self, effect_flag: ObjectEffectFlags, state: bool) -> None:
        self._raw.effect_flags[effect_flag.name] = state

    @property
    def model_id(self) -> int:
        return self._raw.model_id

    @model_id.setter
    def model_id(self, value: int) -> None:
        self._raw.model_id = value

    @property
    def linked_entity(self) -> int:
        return self._raw.linked_entity

    @linked_entity.setter
    def linked_entity(self, value: int) -> None:
        self._raw.linked_entity = value

    @property
    def scan_id(self) -> int:
        return self._raw.scan_id

    @scan_id.setter
    def scan_id(self, value: int) -> None:
        self._raw.scan_id = value

    @property
    def scan_message_target(self) -> int:
        return self._raw.scan_message_target

    @scan_message_target.setter
    def scan_message_target(self, value: int) -> None:
        self._raw.scan_message_target = value

    @property
    def scan_message(self) -> Message:
        return self._raw.scan_message

    @scan_message.setter
    def scan_message(self, value: Message) -> None:
        self._raw.scan_message = value

    @property
    def effect_id(self) -> int:
        return self._raw.effect_id

    @effect_id.setter
    def effect_id(self, value: int) -> None:
        self._raw.effect_id = value

    @property
    def effect_interval(self) -> int:
        return self._raw.effect_interval

    @effect_interval.setter
    def effect_interval(self, value: int) -> None:
        self._raw.effect_interval = value

    @property
    def effect_on_inverals(self) -> int:
        return self._raw.effect_on_inverals

    @effect_on_inverals.setter
    def effect_on_inverals(self, value: int) -> None:
        self._raw.effect_on_inverals = value

    @property
    def effect_position_offset(self) -> Vec3:
        return self._raw.effect_position_offset

    @effect_position_offset.setter
    def effect_position_offset(self, value: Vec3) -> None:
        self._raw.effect_position_offset = value

    def get_volume(self) -> VolumeType:
        return VolumeType(self._raw.volume)
