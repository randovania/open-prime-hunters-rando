import enum

from construct import Byte, Construct, Flag, Int32ul, Struct

from open_prime_hunters_rando.parsing.common_types import PaletteIdConstruct
from open_prime_hunters_rando.parsing.construct_extensions import EnumAdapter
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_file import DecodedString
from open_prime_hunters_rando.parsing.formats.entities.enum import PaletteId


class DoorType(enum.Enum):
    STANDARD = 0
    MORPH_BALL = 1
    BOSS = 2
    THIN = 3


DoorEntityData = Struct(
    "node_name" / DecodedString,
    "palette_id" / PaletteIdConstruct,
    "door_type" / EnumAdapter(DoorType, Int32ul),
    "connector_id" / Int32ul,
    "target_layer_id" / Byte,
    "locked" / Flag,
    "out_connector_id" / Byte,
    "out_loader_id" / Byte,
    "entity_file_name" / DecodedString,
    "room_name" / DecodedString,
)


class Door(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return DoorEntityData

    node_name = field(str)

    palette_id = field(PaletteId)
    door_type = field(DoorType)

    connector_id = field(int)
    target_layer_id = field(int)

    locked = field(bool)

    out_connector_id = field(int)
    out_loader_id = field(int)

    entity_file_name = field(str)
    room_name = field(str)
