from open_prime_hunters_rando.entities.entity_type import Entity
from open_prime_hunters_rando.entities.enum import Message, TriggerVolumeFlags, TriggerVolumeType, VolumeType


class TriggerVolume(Entity):
    @property
    def subtype(self) -> TriggerVolumeType:
        return self._raw.data.subtype

    @subtype.setter
    def subtype(self, value: TriggerVolumeType) -> None:
        self._raw.data.subtype = value

    def get_volume(self) -> VolumeType:
        return VolumeType(self._raw.data.volume)

    @property
    def active(self) -> bool:
        return self._raw.data.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.data.active = value

    @property
    def always_active(self) -> bool:
        return self._raw.data.always_active

    @always_active.setter
    def always_active(self, value: bool) -> None:
        self._raw.data.always_active = value

    @property
    def deactivate_after_use(self) -> bool:
        return self._raw.data.deactivate_after_use

    @deactivate_after_use.setter
    def deactivate_after_use(self, value: bool) -> None:
        self._raw.data.deactivate_after_use = value

    @property
    def repeat_delay(self) -> int:
        return self._raw.data.repeat_delay

    @repeat_delay.setter
    def repeat_delay(self, value: int) -> None:
        self._raw.data.repeat_delay = value

    @property
    def check_delay(self) -> int:
        return self._raw.data.check_delay

    @check_delay.setter
    def check_delay(self, value: int) -> None:
        self._raw.data.check_delay = value

    @property
    def required_state_bit(self) -> int:
        return self._raw.data.required_state_bit

    @required_state_bit.setter
    def required_state_bit(self, value: int) -> None:
        self._raw.data.required_state_bit = value

    def trigger_flags(self, flag: TriggerVolumeFlags) -> bool:
        return self._raw.data.trigger_flags[flag.name]

    def set_trigger_flags(self, flag: TriggerVolumeFlags, state: bool) -> None:
        self._raw.data.trigger_flags[flag.name] = state

    @property
    def trigger_threshold(self) -> int:
        return self._raw.data.trigger_threshold

    @trigger_threshold.setter
    def trigger_threshold(self, value: int) -> None:
        self._raw.data.trigger_threshold = value

    @property
    def parent_id(self) -> int:
        return self._raw.data.parent_id

    @parent_id.setter
    def parent_id(self, value: int) -> None:
        self._raw.data.parent_id = value

    @property
    def parent_message(self) -> Message:
        return self._raw.data.parent_message

    @parent_message.setter
    def parent_message(self, value: Message) -> None:
        self._raw.data.parent_message = value

    @property
    def parent_message_param1(self) -> int:
        return self._raw.data.parent_message_param1

    @parent_message_param1.setter
    def parent_message_param1(self, value: int) -> None:
        self._raw.data.parent_message_param1 = value

    @property
    def parent_message_param2(self) -> int:
        return self._raw.data.parent_message_param2

    @parent_message_param2.setter
    def parent_message_param2(self, value: int) -> None:
        self._raw.data.parent_message_param2 = value

    @property
    def child_id(self) -> int:
        return self._raw.data.child_id

    @child_id.setter
    def child_id(self, value: int) -> None:
        self._raw.data.child_id = value

    @property
    def child_message(self) -> Message:
        return self._raw.data.child_message

    @child_message.setter
    def child_message(self, value: Message) -> None:
        self._raw.data.child_message = value

    @property
    def child_message_param1(self) -> int:
        return self._raw.data.child_message_param1

    @child_message_param1.setter
    def child_message_param1(self, value: int) -> None:
        self._raw.data.child_message_param1 = value

    @property
    def child_message_param2(self) -> int:
        return self._raw.data.child_message_param2

    @child_message_param2.setter
    def child_message_param2(self, value: int) -> None:
        self._raw.data.child_message_param2 = value
