from open_prime_hunters_rando.entities.entity_types.enemy_spawn import EnemySpawn
from open_prime_hunters_rando.entities.enum import VolumeType


class CommonEnemy2FireSpawnSpawnField(EnemySpawn):
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

    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.data.volume0)

    def get_volume1(self) -> VolumeType:
        return VolumeType(self._raw.data.volume1)

    def get_volume2(self) -> VolumeType:
        return VolumeType(self._raw.data.volume2)

    def get_volume3(self) -> VolumeType:
        return VolumeType(self._raw.data.volume3)
