from construct import Construct, Flag, Int16sl, Struct

from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_file import EntityDataHeader

PointModuleEntityData = Struct(
    "header" / EntityDataHeader,
    "next_id" / Int16sl,
    "prev_id" / Int16sl,
    "active" / Flag,
)


class PointModule(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return PointModule

    @property
    def next_id(self) -> int:
        return self._raw.data.next_id

    @next_id.setter
    def next_id(self, value: int) -> None:
        self._raw.data.next_id = value

    @property
    def prev_id(self) -> int:
        return self._raw.data.prev_id

    @prev_id.setter
    def prev_id(self, value: int) -> None:
        self._raw.data.prev_id = value

    @property
    def active(self) -> bool:
        return self._raw.data.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.data.active = value
