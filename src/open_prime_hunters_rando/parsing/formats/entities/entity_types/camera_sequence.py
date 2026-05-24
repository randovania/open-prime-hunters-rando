import typing

from construct import Byte, Construct, Flag, Int16sl, Int16ul, Int32sl, Struct

from open_prime_hunters_rando.parsing.common_types import MessageConstruct
from open_prime_hunters_rando.parsing.common_types.vectors import Vec3
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType, Message

CameraSequenceEntityData = Struct(
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

    sequence_id = field(int)

    handoff = field(bool)
    loop = field(bool)
    block_input = field(bool)

    force_alt_form = field(bool)
    force_biped_form = field(bool)

    delay_frames = field(int)

    player_id1 = field(int)
    player_id2 = field(int)

    entity1 = field(int)
    entity2 = field(int)

    end_message_target_id = field(int)
    end_message = field(Message)
    end_message_param = field(int)

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.CAMERA_SEQUENCE

    @classmethod
    def create(
        cls,
        node_name: str = "",
        layer_state: typing.Sequence[bool | int] = (False,) * 16,
        entity_id: int = -1,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 1.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 1.0),
        sequence_id: int = 0,
        handoff: bool = False,
        loop: bool = False,
        block_input: bool = True,
        force_alt_form: bool = False,
        force_biped_form: bool = True,
        delay_frames: int = 0,
        player_id1: int = 0,
        player_id2: int = 0,
        entity1: int = -1,
        entity2: int = -1,
        end_message_target_id: int = -1,
        end_message: Message = Message.NONE,
        end_message_param: int = 0,
    ) -> typing.Self:
        obj = super().create(
            node_name,
            layer_state,
            entity_id,
            position,
            up_vector,
            facing_vector,
        )
        obj.sequence_id = sequence_id
        obj.handoff = handoff
        obj.loop = loop
        obj.block_input = block_input
        obj.force_alt_form = force_alt_form
        obj.force_biped_form = force_biped_form
        obj.delay_frames = delay_frames
        obj.player_id1 = player_id1
        obj.player_id2 = player_id2
        obj.entity1 = entity1
        obj.entity2 = entity2
        obj.end_message_target_id = end_message_target_id
        obj.end_message = end_message
        obj.end_message_param = end_message_param

        return obj
