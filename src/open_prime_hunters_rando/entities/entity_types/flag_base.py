from open_prime_hunters_rando.entities.entity_type import Entity
from open_prime_hunters_rando.entities.enum import VolumeType


class FlagBase(Entity):
    @property
    def team_id(self) -> int:
        return self._raw.data.team_id

    @team_id.setter
    def team_id(self, value: int) -> None:
        self._raw.data.team_id = value

    def get_volume(self) -> VolumeType:
        return VolumeType(self._raw.data.volume)
