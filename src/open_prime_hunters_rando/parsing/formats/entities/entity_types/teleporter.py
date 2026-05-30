import typing

from construct import Byte, Construct, Flag, Int32ul, PaddedString, Struct

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_file import DecodedString, Vector3Fx
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType

TeleporterEntityData = Struct(
    "load_index" / Byte,
    "target_index" / Byte,
    "artifact_id" / Byte,
    "active" / Flag,
    "invisible" / Flag,
    "entity_filename" / PaddedString(15, "ascii"),
    "field7" / Int32ul,  # Unused
    "target_position" / Vector3Fx,
    "teleporter_node_name" / DecodedString,
)


class Teleporter(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return TeleporterEntityData

    load_index = field(int)
    target_index = field(int)
    artifact_id = field(int)

    active = field(bool)
    invisible = field(bool)

    entity_filename = field(str)

    field7 = field(int)

    target_position = field(Vec3)

    teleporter_node_name = field(str)

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.TELEPORTER

    @classmethod
    def create(
        cls,
        node_name: str = "",
        layer_state: typing.Sequence[bool] = (False,) * 16,
        entity_id: int = -1,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 1.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 1.0),
        load_index: int = 0,
        target_index: int = 0,
        artifact_id: int = 0,
        active: bool = True,
        invisible: bool = True,
        entity_filename: str = "",
        field7: int = 4294901760,
        target_position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        teleporter_node_name: str = "",
    ) -> typing.Self:
        obj = super().create(
            node_name,
            layer_state,
            entity_id,
            position,
            up_vector,
            facing_vector,
        )
        obj.load_index = load_index
        obj.target_index = target_index
        obj.artifact_id = artifact_id
        obj.active = active
        obj.invisible = invisible
        obj.entity_filename = entity_filename
        obj.field7 = field7
        obj.target_position = Vec3(*target_position)
        obj.teleporter_node_name = teleporter_node_name

        return obj
