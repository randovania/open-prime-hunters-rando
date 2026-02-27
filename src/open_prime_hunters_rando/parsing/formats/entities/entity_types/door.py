import enum

from construct import Byte, Construct, Flag, Int32ul, Struct

from open_prime_hunters_rando.common import EnumAdapter
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_file import DecodedString, EntityDataHeader, PaletteIdConstruct
from open_prime_hunters_rando.parsing.formats.entities.enum import PaletteId


class DoorType(enum.Enum):
    STANDARD = 0
    MORPH_BALL = 1
    BOSS = 2
    THIN = 3


DoorEntityData = Struct(
    "header" / EntityDataHeader,
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

    @property
    def node_name(self) -> str:
        return self._raw.data.node_name

    @node_name.setter
    def node_name(self, value: str) -> None:
        self._raw.data.node_name = value

    @property
    def palette_id(self) -> PaletteId:
        return self._raw.data.palette_id

    @palette_id.setter
    def palette_id(self, value: PaletteId) -> None:
        self._raw.data.palette_id = value

    @property
    def door_type(self) -> DoorType:
        return self._raw.data.palette_id

    @door_type.setter
    def door_type(self, value: DoorType) -> None:
        self._raw.data.door_type = value

    @property
    def connector_id(self) -> int:
        return self._raw.data.connector_id

    @connector_id.setter
    def connector_id(self, value: int) -> None:
        self._raw.data.connector_id = value

    @property
    def target_layer_id(self) -> int:
        return self._raw.data.target_layer_id

    @target_layer_id.setter
    def target_layer_id(self, value: int) -> None:
        self._raw.data.target_layer_id = value

    @property
    def locked(self) -> bool:
        return self._raw.data.locked

    @locked.setter
    def locked(self, value: bool) -> None:
        self._raw.data.locked = value

    @property
    def out_connector_id(self) -> int:
        return self._raw.data.out_connector_id

    @out_connector_id.setter
    def out_connector_id(self, value: int) -> None:
        self._raw.data.out_connector_id = value

    @property
    def out_loader_id(self) -> int:
        return self._raw.data.out_loader_id

    @out_loader_id.setter
    def out_loader_id(self, value: int) -> None:
        self._raw.data.out_loader_id = value

    @property
    def entity_file_name(self) -> str:
        return self._raw.data.entity_file_name

    @entity_file_name.setter
    def entity_file_name(self, value: str) -> None:
        self._raw.data.entity_file_name = value

    @property
    def room_name(self) -> str:
        return self._raw.data.room_name

    @room_name.setter
    def room_name(self, value: str) -> None:
        self._raw.data.room_name = value
