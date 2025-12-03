from construct import Container

from open_prime_hunters_rando.entities.entity_type import Message, TriggerVolumeFlags, VolumeType


class AreaVolume:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def get_volume(self) -> VolumeType:
        return VolumeType(self._raw.volume)

    @property
    def active(self) -> bool:
        return self._raw.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.active = value

    @property
    def always_active(self) -> bool:
        return self._raw.always_active

    @always_active.setter
    def always_active(self, value: bool) -> None:
        self._raw.always_active = value

    @property
    def allow_mulitple(self) -> bool:
        return self._raw.allow_mulitple

    @allow_mulitple.setter
    def allow_mulitple(self, value: bool) -> None:
        self._raw.allow_mulitple = value

    @property
    def message_delay(self) -> int:
        return self._raw.message_delay

    @message_delay.setter
    def message_delay(self, value: int) -> None:
        self._raw.message_delay = value

    @property
    def inside_message(self) -> Message:
        return self._raw.inside_message

    @inside_message.setter
    def inside_message(self, value: Message) -> None:
        self._raw.inside_message = value

    @property
    def inside_message_param1(self) -> int:
        return self._raw.inside_message_param1

    @inside_message_param1.setter
    def inside_message_param1(self, value: int) -> None:
        self._raw.inside_message_param1 = value

    @property
    def inside_message_param2(self) -> int:
        return self._raw.inside_message_param2

    @inside_message_param2.setter
    def inside_message_param2(self, value: int) -> None:
        self._raw.inside_message_param2 = value

    @property
    def parent_id(self) -> int:
        return self._raw.parent_id

    @parent_id.setter
    def parent_id(self, value: int) -> None:
        self._raw.parent_id = value

    @property
    def exit_message(self) -> Message:
        return self._raw.exit_message

    @exit_message.setter
    def exit_message(self, value: Message) -> None:
        self._raw.exit_message = value

    @property
    def exit_message_param1(self) -> int:
        return self._raw.exit_message_param1

    @exit_message_param1.setter
    def exit_message_param1(self, value: int) -> None:
        self._raw.exit_message_param1 = value

    @property
    def exit_message_param2(self) -> int:
        return self._raw.exit_message_param2

    @exit_message_param2.setter
    def exit_message_param2(self, value: int) -> None:
        self._raw.exit_message_param2 = value

    @property
    def child_id(self) -> int:
        return self._raw.child_id

    @child_id.setter
    def child_id(self, value: int) -> None:
        self._raw.child_id = value

    @property
    def cooldown(self) -> int:
        return self._raw.cooldown

    @cooldown.setter
    def cooldown(self, value: int) -> None:
        self._raw.cooldown = value

    @property
    def priority(self) -> int:
        return self._raw.priority

    @priority.setter
    def priority(self, value: int) -> None:
        self._raw.priority = value

    def trigger_flags(self, flag: TriggerVolumeFlags) -> bool:
        return self._raw.trigger_flags[flag.name]

    def set_trigger_flags(self, flag: TriggerVolumeFlags, state: bool) -> None:
        self._raw.trigger_flags[flag.name] = state
