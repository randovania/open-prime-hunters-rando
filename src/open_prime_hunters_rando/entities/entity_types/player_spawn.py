from construct import Byte, Construct, Struct

from open_prime_hunters_rando.entities.entity import Entity
from open_prime_hunters_rando.entities.entity_file import EntityDataHeader

PlayerSpawnEntityData = Struct(
    "header" / EntityDataHeader,
    "availability" / Byte,
    "active" / Byte,
    "team_index" / Byte,
)


class PlayerSpawn(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return PlayerSpawnEntityData

    @property
    def availability(self) -> int:
        return self._raw.data.availability

    @availability.setter
    def availability(self, value: int) -> None:
        self._raw.data.availability = value

    @property
    def active(self) -> int:
        return self._raw.data.active

    @active.setter
    def active(self, value: int) -> None:
        self._raw.data.active = value

    @property
    def team_index(self) -> int:
        return self._raw.data.team_index

    @team_index.setter
    def team_index(self, value: int) -> None:
        self._raw.data.team_index = value
