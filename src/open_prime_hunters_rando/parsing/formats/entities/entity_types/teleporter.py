from construct import Byte, Construct, Flag, Int32ul, PaddedString, Struct

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_file import DecodedString, Vector3Fx

TeleporterEntityData = Struct(
    "load_index" / Byte,
    "target_index" / Byte,
    "artifact_id" / Byte,
    "active" / Flag,
    "invisible" / Flag,
    "entity_filename" / PaddedString(15, "ascii"),
    "_unused" / Int32ul,
    "target_position" / Vector3Fx,
    "node_name" / DecodedString,
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

    target_position = field(Vec3)

    node_name = field(str)
