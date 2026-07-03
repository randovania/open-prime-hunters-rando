import copy
import enum
import typing
from typing import Any, Self

import construct
from construct import (
    Array,
    Byte,
    Container,
    Flag,
    Int16sl,
    Int16ul,
    Int32ul,
    ListContainer,
    Struct,
    this,
)

from open_prime_hunters_rando.parsing.common_types import (
    DecodedString,
    FixedPoint,
)
from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.construct_extensions import EnumAdapter
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType, Message


class FadeType(enum.Enum):
    NONE = 0
    FADE_IN_BLACK = 1
    FADE_OUT_BLACK = 2
    FADE_IN_WHITE = 3
    FADE_OUT_WHITE = 4
    FADE_OUT_IN_BLACK = 5
    FADE_OUT_IN_WHITE = 6


FadeTypeConstruct = EnumAdapter(FadeType, Byte)

EntityTypeConstruct = EnumAdapter(EntityType, Int16sl)

Header = Struct(
    "count" / Int16ul,
    "version" / Byte,
    "_padding1" / Byte,
    "_padding2" / Int32ul,
)

RawKeyFrameEntry = Struct(
    "position" / Vector3Fx,
    "to_target" / Vector3Fx,
    "roll" / FixedPoint,
    "fov" / FixedPoint,
    "move_time" / FixedPoint,
    "hold_time" / FixedPoint,
    "fade_in_time" / FixedPoint,
    "fade_out_time" / FixedPoint,
    "fade_in_type" / FadeTypeConstruct,
    "fade_out_type" / FadeTypeConstruct,
    "previous_frame_influence" / Byte,
    "after_frame_influence" / Byte,
    "use_entity_transform" / Flag,
    "_padding1" / Byte,
    "_padding2" / Int16ul,
    "pos_entity_type" / EntityTypeConstruct,
    "pos_entity_id" / Int16sl,
    "target_entity_type" / EntityTypeConstruct,
    "target_entity_id" / Int16sl,
    "message_target_type" / EntityTypeConstruct,
    "message_target_id" / Int16sl,
    "message_id" / EnumAdapter(Message, Int16ul),
    "message_param" / Int16ul,
    "easing" / FixedPoint,
    "_unused1" / Int32ul,
    "_unused2" / Int32ul,
    "node_name" / DecodedString,
)

CameraSequenceFileConstruct = Struct(
    "header" / Header,
    "keyframes" / Array(this.header.count, RawKeyFrameEntry),
)


class CameraSequenceFileAdapter(construct.Adapter):
    def __init__(self) -> None:
        super().__init__(CameraSequenceFileConstruct)

    def _decode(self, obj: Container, context: Container, path: str) -> Container:
        decoded = copy.deepcopy(obj)

        # wrap keyframes
        decoded.keyframes = ListContainer([KeyFrameEntry(keyframe) for keyframe in decoded.keyframes])

        return decoded

    def _encode(self, obj: Container, context: Container, path: str) -> Container:
        encoded = copy.deepcopy(obj)

        keyframes = typing.cast("list[KeyFrameEntry]", encoded.keyframes)

        encoded.keyframes = ListContainer()

        for keyframe_wrapper in keyframes:
            keyframe = keyframe_wrapper._raw

            encoded.keyframes.append(keyframe)

        return encoded


class KeyFrameEntry:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def __repr__(self) -> str:
        return f"<Keyframe data={self._raw}"

    def __hash__(self) -> int:
        return hash(self._raw)

    @property
    def position(self) -> Vec3:
        return self._raw.position

    @position.setter
    def position(self, value: Vec3) -> None:
        self._raw.position = value

    @property
    def to_target(self) -> Vec3:
        return self._raw.to_target

    @to_target.setter
    def to_target(self, value: Vec3) -> None:
        self._raw.to_target = value

    @property
    def roll(self) -> float:
        return self._raw.roll

    @roll.setter
    def roll(self, value: float) -> None:
        self._raw.roll = value

    @property
    def fov(self) -> float:
        return self._raw.fov

    @fov.setter
    def fov(self, value: float) -> None:
        self._raw.fov = value

    @property
    def move_time(self) -> float:
        return self._raw.move_time

    @move_time.setter
    def move_time(self, value: float) -> None:
        self._raw.move_time = value

    @property
    def hold_time(self) -> float:
        return self._raw.hold_time

    @hold_time.setter
    def hold_time(self, value: float) -> None:
        self._raw.hold_time = value

    @property
    def fade_in_time(self) -> float:
        return self._raw.fade_in_time

    @fade_in_time.setter
    def fade_in_time(self, value: float) -> None:
        self._raw.fade_in_time = value

    @property
    def fade_out_time(self) -> float:
        return self._raw.fade_out_time

    @fade_out_time.setter
    def fade_out_time(self, value: float) -> None:
        self._raw.fade_out_time = value

    @property
    def fade_in_type(self) -> FadeType:
        return self._raw.fade_in_type

    @fade_in_type.setter
    def fade_in_type(self, value: FadeType) -> None:
        self._raw.fade_in_type = value

    @property
    def fade_out_type(self) -> FadeType:
        return self._raw.fade_out_type

    @fade_out_type.setter
    def fade_out_type(self, value: FadeType) -> None:
        self._raw.fade_out_type = value

    @property
    def previous_frame_influence(self) -> int:
        return self._raw.previous_frame_influence

    @previous_frame_influence.setter
    def previous_frame_influence(self, value: int) -> None:
        self._raw.previous_frame_influence = value

    @property
    def after_frame_influence(self) -> int:
        return self._raw.after_frame_influence

    @after_frame_influence.setter
    def after_frame_influence(self, value: int) -> None:
        self._raw.after_frame_influence = value

    @property
    def use_entity_transform(self) -> bool:
        return self._raw.use_entity_transform

    @use_entity_transform.setter
    def use_entity_transform(self, value: bool) -> None:
        self._raw.use_entity_transform = value

    @property
    def pos_entity_type(self) -> EntityType:
        return self._raw.pos_entity_type

    @pos_entity_type.setter
    def pos_entity_type(self, value: EntityType) -> None:
        self._raw.pos_entity_type = value

    @property
    def pos_entity_id(self) -> int:
        return self._raw.pos_entity_id

    @pos_entity_id.setter
    def pos_entity_id(self, value: int) -> None:
        self._raw.pos_entity_id = value

    @property
    def target_entity_type(self) -> EntityType:
        return self._raw.target_entity_type

    @target_entity_type.setter
    def target_entity_type(self, value: EntityType) -> None:
        self._raw.target_entity_type = value

    @property
    def target_entity_id(self) -> int:
        return self._raw.target_entity_id

    @target_entity_id.setter
    def target_entity_id(self, value: int) -> None:
        self._raw.target_entity_id = value

    @property
    def message_target_type(self) -> EntityType:
        return self._raw.message_target_type

    @message_target_type.setter
    def message_target_type(self, value: EntityType) -> None:
        self._raw.message_target_type = value

    @property
    def message_target_id(self) -> int:
        return self._raw.message_target_id

    @message_target_id.setter
    def message_target_id(self, value: int) -> None:
        self._raw.message_target_id = value

    @property
    def message_id(self) -> Message:
        return self._raw.message_id

    @message_id.setter
    def message_id(self, value: Message) -> None:
        self._raw.message_id = value

    @property
    def message_param(self) -> int:
        return self._raw.message_param

    @message_param.setter
    def message_param(self, value: int) -> None:
        self._raw.message_param = value

    @property
    def easing(self) -> float:
        return self._raw.easing

    @easing.setter
    def easing(self, value: float) -> None:
        self._raw.easing = value

    @property
    def node_name(self) -> str:
        return self._raw.node_name

    @node_name.setter
    def node_name(self, value: str) -> None:
        self._raw.node_name = value


class CameraSequenceFile:
    def __init__(self, raw: Container):
        self._raw = raw

    @classmethod
    def parse(cls, data: bytes) -> Self:
        # parse
        data = bytes(data)

        return cls(CameraSequenceFileAdapter().parse(data))

    def build(self) -> bytes:
        # update amount of entries
        self._raw.header.count = len(self.keyframes)

        # build
        data = CameraSequenceFileAdapter().build(self._raw)

        return data

    def __eq__(self, value: Any) -> bool:
        return isinstance(value, CameraSequenceFile) and self.keyframes == value.keyframes

    def __hash__(self) -> int:
        return hash(self._raw)

    @property
    def count(self) -> int:
        return self._raw.header.count

    @property
    def keyframes(self) -> list[KeyFrameEntry]:
        return self._raw.keyframes

    @keyframes.setter
    def keyframes(self, value: list[KeyFrameEntry]) -> None:
        self._raw.keyframes = value
