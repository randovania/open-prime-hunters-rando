from construct import Byte, Construct, Flag, Int16sl, Int16ul, Int32sl, Struct

from open_prime_hunters_rando.parsing.common_types import MessageConstruct
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.enum import Message

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
