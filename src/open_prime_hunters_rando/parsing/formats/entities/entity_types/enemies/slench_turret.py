from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemy_spawn import EnemySpawn
from open_prime_hunters_rando.parsing.formats.entities.enum import VolumeTypeCommon


class SlenchTurretSpawnField(EnemySpawn):
    @property
    def enemy_subtype(self) -> int:
        return self._raw.data.enemy_subtype

    @enemy_subtype.setter
    def enemy_subtype(self, value: int) -> None:
        self._raw.data.enemy_subtype = value

    @property
    def enemy_version(self) -> int:
        return self._raw.data.enemy_version

    @enemy_version.setter
    def enemy_version(self, value: int) -> None:
        self._raw.data.enemy_version = value

    def get_volume0(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume0)

    def get_volume1(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume1)

    @property
    def index(self) -> int:
        return self._raw.data.index

    @index.setter
    def index(self, value: int) -> None:
        self._raw.data.index = value
