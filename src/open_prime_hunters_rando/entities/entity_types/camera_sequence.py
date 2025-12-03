from construct import Container

from open_prime_hunters_rando.entities.enum import Message


class CameraSequence:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def sequence_id(self) -> int:
        return self._raw.sequence_id

    @sequence_id.setter
    def sequence_id(self, value: int) -> None:
        self._raw.sequence_id = value

    @property
    def handoff(self) -> bool:
        return self._raw.handoff

    @handoff.setter
    def handoff(self, value: bool) -> None:
        self._raw.handoff = value

    @property
    def loop(self) -> bool:
        return self._raw.loop

    @loop.setter
    def loop(self, value: bool) -> None:
        self._raw.loop = value

    @property
    def block_input(self) -> bool:
        return self._raw.block_input

    @block_input.setter
    def block_input(self, value: bool) -> None:
        self._raw.block_input = value

    @property
    def force_alt_form(self) -> bool:
        return self._raw.force_alt_form

    @force_alt_form.setter
    def force_alt_form(self, value: bool) -> None:
        self._raw.force_alt_form = value

    @property
    def force_biped_form(self) -> bool:
        return self._raw.force_biped_form

    @force_biped_form.setter
    def force_biped_form(self, value: bool) -> None:
        self._raw.force_biped_form = value

    @property
    def delay_frames(self) -> int:
        return self._raw.delay_frames

    @delay_frames.setter
    def delay_frames(self, value: int) -> None:
        self._raw.delay_frames = value

    @property
    def player_id1(self) -> int:
        return self._raw.player_id1

    @player_id1.setter
    def player_id1(self, value: int) -> None:
        self._raw.player_id1 = value

    @property
    def player_id2(self) -> int:
        return self._raw.player_id2

    @player_id2.setter
    def player_id2(self, value: int) -> None:
        self._raw.player_id2 = value

    @property
    def entity1(self) -> int:
        return self._raw.entity1

    @entity1.setter
    def entity1(self, value: int) -> None:
        self._raw.entity1 = value

    @property
    def entity2(self) -> int:
        return self._raw.entity2

    @entity2.setter
    def entity2(self, value: int) -> None:
        self._raw.entity2 = value

    @property
    def end_message_target_id(self) -> int:
        return self._raw.end_message_target_id

    @end_message_target_id.setter
    def end_message_target_id(self, value: int) -> None:
        self._raw.end_message_target_id = value

    @property
    def end_message(self) -> Message:
        return self._raw.end_message

    @end_message.setter
    def end_message(self, value: Message) -> None:
        self._raw.end_message = value

    @property
    def end_message_param(self) -> int:
        return self._raw.end_message_param

    @end_message_param.setter
    def end_message_param(self, value: int) -> None:
        self._raw.end_message_param = value
