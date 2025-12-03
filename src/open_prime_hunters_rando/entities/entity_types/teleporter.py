from construct import Container

from open_prime_hunters_rando.entities.vec import Vec3


class Teleporter:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def load_index(self) -> int:
        return self._raw.load_index

    @load_index.setter
    def load_index(self, value: int) -> None:
        self._raw.load_index = value

    @property
    def target_index(self) -> int:
        return self._raw.target_index

    @target_index.setter
    def target_index(self, value: int) -> None:
        self._raw.target_index = value

    @property
    def artifact_id(self) -> int:
        return self._raw.artifact_id

    @artifact_id.setter
    def artifact_id(self, value: int) -> None:
        self._raw.artifact_id = value

    @property
    def active(self) -> bool:
        return self._raw.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.active = value

    @property
    def invisible(self) -> bool:
        return self._raw.invisible

    @invisible.setter
    def invisible(self, value: bool) -> None:
        self._raw.invisible = value

    @property
    def entity_filename(self) -> str:
        return self._raw.entity_filename

    @entity_filename.setter
    def entity_filename(self, value: str) -> None:
        self._raw.entity_filename = value

    @property
    def target_position(self) -> Vec3:
        return self._raw.target_position

    @target_position.setter
    def target_position(self, value: Vec3) -> None:
        self._raw.target_position = value

    @property
    def node_name(self) -> str:
        return self._raw.node_name

    @node_name.setter
    def node_name(self, value: str) -> None:
        self._raw.node_name = value
