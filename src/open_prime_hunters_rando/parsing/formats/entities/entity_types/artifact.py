import typing

from construct import Byte, Construct, Flag, Int16sl, Padded, Struct

from open_prime_hunters_rando.common import Vec3
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_file import MessageConstruct
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType, Message

ArtifactEntityData = Struct(
    "model_id" / Byte,
    "artifact_id" / Byte,
    "active" / Flag,
    "has_base" / Flag,
    "message1_target" / Padded(4, Int16sl),
    "message1" / MessageConstruct,
    "message2_target" / Padded(4, Int16sl),
    "message2" / MessageConstruct,
    "message3_target" / Padded(4, Int16sl),
    "message3" / MessageConstruct,
    "linked_entity_id" / Int16sl,
)


class Artifact(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return ArtifactEntityData

    model_id = field(int)
    artifact_id = field(int)

    active = field(bool)
    has_base = field(bool)

    message1_target = field(int)
    message1 = field(Message)

    message2_target = field(int)
    message2 = field(Message)

    message3_target = field(int)
    message3 = field(Message)

    linked_entity_id = field(int)

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.ARTIFACT

    @classmethod
    def create(
        cls,
        node_name: str = "",
        layer_state: typing.Sequence[bool] = (False,) * 16,
        entity_id: int = -1,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        model_id: int = 0,
        artifact_id: int = 0,
        active: bool = True,
        has_base: bool = False,
        message1_target: int = 0,
        message1: Message = Message.NONE,
        message2_target: int = 0,
        message2: Message = Message.NONE,
        message3_target: int = 0,
        message3: Message = Message.NONE,
        linked_entity_id: int = 0,
    ) -> typing.Self:
        obj = super().create(
            node_name,
            layer_state,
            entity_id,
            position,
            up_vector,
            facing_vector,
        )
        obj.model_id = model_id
        obj.artifact_id = artifact_id
        obj.active = active
        obj.has_base = has_base
        obj.message1 = message1
        obj.message1_target = message1_target
        obj.message2 = message2
        obj.message2_target = message2_target
        obj.message3 = message3
        obj.message3_target = message3_target
        obj.linked_entity_id = linked_entity_id

        return obj
