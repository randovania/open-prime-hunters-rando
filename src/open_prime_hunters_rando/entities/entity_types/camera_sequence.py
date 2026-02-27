from construct import Byte, Construct, Flag, Int16sl, Int16ul, Int32sl, Struct

from open_prime_hunters_rando.entities.entity import Entity
from open_prime_hunters_rando.entities.entity_file import EntityDataHeader, MessageConstruct
from open_prime_hunters_rando.entities.enum import Message

CameraSequenceEntityData = Struct(
    "header" / EntityDataHeader,
    "sequence_id" / Byte,
    "handoff" / Flag,
    "loop" / Flag,
    "block_input" / Flag,
    "force_alt_form" / Flag,
    "force_biped_form" / Flag,
    "delay_frames" / Int16ul,
    "player_id1" / Byte,
    "player_id2" / Byte,
    "entity1" / Int16sl,
    "entity2" / Int16sl,
    "end_message_target_id" / Int16sl,
    "end_message" / MessageConstruct,
    "end_message_param" / Int32sl,
)


class CameraSequence(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return CameraSequenceEntityData

    @property
    def sequence_id(self) -> int:
        return self._raw.data.sequence_id

    @sequence_id.setter
    def sequence_id(self, value: int) -> None:
        self._raw.data.sequence_id = value

    @property
    def handoff(self) -> bool:
        return self._raw.data.handoff

    @handoff.setter
    def handoff(self, value: bool) -> None:
        self._raw.data.handoff = value

    @property
    def loop(self) -> bool:
        return self._raw.data.loop

    @loop.setter
    def loop(self, value: bool) -> None:
        self._raw.data.loop = value

    @property
    def block_input(self) -> bool:
        return self._raw.data.block_input

    @block_input.setter
    def block_input(self, value: bool) -> None:
        self._raw.data.block_input = value

    @property
    def force_alt_form(self) -> bool:
        return self._raw.data.force_alt_form

    @force_alt_form.setter
    def force_alt_form(self, value: bool) -> None:
        self._raw.data.force_alt_form = value

    @property
    def force_biped_form(self) -> bool:
        return self._raw.data.force_biped_form

    @force_biped_form.setter
    def force_biped_form(self, value: bool) -> None:
        self._raw.data.force_biped_form = value

    @property
    def delay_frames(self) -> int:
        return self._raw.data.delay_frames

    @delay_frames.setter
    def delay_frames(self, value: int) -> None:
        self._raw.data.delay_frames = value

    @property
    def player_id1(self) -> int:
        return self._raw.data.player_id1

    @player_id1.setter
    def player_id1(self, value: int) -> None:
        self._raw.data.player_id1 = value

    @property
    def player_id2(self) -> int:
        return self._raw.data.player_id2

    @player_id2.setter
    def player_id2(self, value: int) -> None:
        self._raw.data.player_id2 = value

    @property
    def entity1(self) -> int:
        return self._raw.data.entity1

    @entity1.setter
    def entity1(self, value: int) -> None:
        self._raw.data.entity1 = value

    @property
    def entity2(self) -> int:
        return self._raw.data.entity2

    @entity2.setter
    def entity2(self, value: int) -> None:
        self._raw.data.entity2 = value

    @property
    def end_message_target_id(self) -> int:
        return self._raw.data.end_message_target_id

    @end_message_target_id.setter
    def end_message_target_id(self, value: int) -> None:
        self._raw.data.end_message_target_id = value

    @property
    def end_message(self) -> Message:
        return self._raw.data.end_message

    @end_message.setter
    def end_message(self, value: Message) -> None:
        self._raw.data.end_message = value

    @property
    def end_message_param(self) -> int:
        return self._raw.data.end_message_param

    @end_message_param.setter
    def end_message_param(self, value: int) -> None:
        self._raw.data.end_message_param = value
