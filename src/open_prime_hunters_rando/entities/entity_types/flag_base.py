from construct import Container

from open_prime_hunters_rando.entities.entity_type import VolumeType


class FlagBase:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def team_id(self) -> int:
        return self._raw.team_id

    @team_id.setter
    def team_id(self, value: int) -> None:
        self._raw.team_id = value

    def get_volume(self) -> VolumeType:
        return VolumeType(self._raw.volume)
