from construct import Byte, Construct, Struct

from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_file import EntityDataHeader

OctolithFlagEntityData = Struct(
    "header" / EntityDataHeader,
    "team_id" / Byte,
)


class OctolithFlag(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return OctolithFlagEntityData

    @property
    def team_id(self) -> int:
        return self._raw.data.team_id

    @team_id.setter
    def team_id(self, value: int) -> None:
        self._raw.data.team_id = value
