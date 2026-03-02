import enum
import typing

from construct import Byte, Construct, Flag, Int32ul, Struct

from open_prime_hunters_rando.parsing.common_types import PaletteIdConstruct
from open_prime_hunters_rando.parsing.common_types.vectors import Vec3
from open_prime_hunters_rando.parsing.construct_extensions import EnumAdapter
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_file import DecodedString
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType, PaletteId


class DoorType(enum.Enum):
    STANDARD = 0
    MORPH_BALL = 1
    BOSS = 2
    THIN = 3


DoorEntityData = Struct(
    "port_name" / DecodedString,
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

    port_name = field(str)

    palette_id = field(PaletteId)
    door_type = field(DoorType)

    connector_id = field(int)
    target_layer_id = field(int)

    locked = field(bool)

    out_connector_id = field(int)
    out_loader_id = field(int)

    entity_file_name = field(str)
    room_name = field(str)

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.DOOR

    @classmethod
    def create(
        cls,
        node_name: str = "",
        layer_state: typing.Sequence[bool] = (False,) * 16,
        entity_id: int = -1,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        port_name: str = "",
        palette_id: PaletteId = PaletteId.POWER_BEAM,
        door_type: DoorType = DoorType.STANDARD,
        connector_id: int = 0,
        target_layer_id: int = 0,
        locked: bool = False,
        out_connector_id: int = 0,
        out_loader_id: int = 0,
        entity_file_name: str = "",
        room_name: str = "",
    ) -> typing.Self:
        obj = super().create(
            node_name,
            layer_state,
            entity_id,
            position,
            up_vector,
            facing_vector,
        )
        obj.port_name = port_name
        obj.palette_id = palette_id
        obj.door_type = door_type
        obj.door_type = door_type
        obj.connector_id = connector_id
        obj.target_layer_id = target_layer_id
        obj.locked = locked
        obj.out_connector_id = out_connector_id
        obj.out_loader_id = out_loader_id
        obj.entity_file_name = entity_file_name
        obj.room_name = room_name

        return obj
