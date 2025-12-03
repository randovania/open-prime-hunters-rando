from construct import Container

from open_prime_hunters_rando.entities.enum import DoorType, PaletteId


class Door:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def node_name(self) -> str:
        return self._raw.node_name

    @node_name.setter
    def node_name(self, value: str) -> None:
        self._raw.node_name = value

    @property
    def palette_id(self) -> PaletteId:
        return self._raw.palette_id

    @palette_id.setter
    def palette_id(self, value: PaletteId) -> None:
        self._raw.palette_id = value

    @property
    def door_type(self) -> DoorType:
        return self._raw.palette_id

    @door_type.setter
    def door_type(self, value: DoorType) -> None:
        self._raw.door_type = value

    @property
    def connector_id(self) -> int:
        return self._raw.connector_id

    @connector_id.setter
    def connector_id(self, value: int) -> None:
        self._raw.connector_id = value

    @property
    def target_layer_id(self) -> int:
        return self._raw.target_layer_id

    @target_layer_id.setter
    def target_layer_id(self, value: int) -> None:
        self._raw.target_layer_id = value

    @property
    def locked(self) -> bool:
        return self._raw.locked

    @locked.setter
    def locked(self, value: bool) -> None:
        self._raw.locked = value

    @property
    def out_connector_id(self) -> int:
        return self._raw.out_connector_id

    @out_connector_id.setter
    def out_connector_id(self, value: int) -> None:
        self._raw.out_connector_id = value

    @property
    def out_loader_id(self) -> int:
        return self._raw.out_loader_id

    @out_loader_id.setter
    def out_loader_id(self, value: int) -> None:
        self._raw.out_loader_id = value

    @property
    def entity_file_name(self) -> str:
        return self._raw.entity_file_name

    @entity_file_name.setter
    def entity_file_name(self, value: str) -> None:
        self._raw.entity_file_name = value

    @property
    def room_name(self) -> str:
        return self._raw.room_name

    @room_name.setter
    def room_name(self, value: str) -> None:
        self._raw.room_name = value
