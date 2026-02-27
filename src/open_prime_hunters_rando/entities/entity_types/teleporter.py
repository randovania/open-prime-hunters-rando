from construct import Byte, Construct, Flag, Int16ul, PaddedString, Struct

from open_prime_hunters_rando.common import Vec3
from open_prime_hunters_rando.entities.entity import Entity
from open_prime_hunters_rando.entities.entity_file import DecodedString, EntityDataHeader, Vector3Fx

TeleporterEntityData = Struct(
    "header" / EntityDataHeader,
    "load_index" / Byte,
    "target_index" / Byte,
    "artifact_id" / Byte,
    "active" / Flag,
    "invisible" / Flag,
    "entity_filename" / PaddedString(15, "ascii"),
    "_unused" / Int16ul[2],
    "target_position" / Vector3Fx,
    "node_name" / DecodedString,
)


class Teleporter(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return TeleporterEntityData

    @property
    def load_index(self) -> int:
        return self._raw.data.load_index

    @load_index.setter
    def load_index(self, value: int) -> None:
        self._raw.data.load_index = value

    @property
    def target_index(self) -> int:
        return self._raw.data.target_index

    @target_index.setter
    def target_index(self, value: int) -> None:
        self._raw.data.target_index = value

    @property
    def artifact_id(self) -> int:
        return self._raw.data.artifact_id

    @artifact_id.setter
    def artifact_id(self, value: int) -> None:
        self._raw.data.artifact_id = value

    @property
    def active(self) -> bool:
        return self._raw.data.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.data.active = value

    @property
    def invisible(self) -> bool:
        return self._raw.data.invisible

    @invisible.setter
    def invisible(self, value: bool) -> None:
        self._raw.data.invisible = value

    @property
    def entity_filename(self) -> str:
        return self._raw.data.entity_filename

    @entity_filename.setter
    def entity_filename(self, value: str) -> None:
        self._raw.data.entity_filename = value

    @property
    def target_position(self) -> Vec3:
        return self._raw.data.target_position

    @target_position.setter
    def target_position(self, value: Vec3) -> None:
        self._raw.data.target_position = value

    @property
    def node_name(self) -> str:
        return self._raw.data.node_name

    @node_name.setter
    def node_name(self, value: str) -> None:
        self._raw.data.node_name = value
