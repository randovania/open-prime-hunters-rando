from open_prime_hunters_rando.entities.entity_types.enemy_spawn import EnemySpawn
from open_prime_hunters_rando.entities.enum import VolumeTypeCommon


class CommonEnemy1SlenchSpawnField(EnemySpawn):
    def get_volume0(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume0)

    def get_volume1(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume1)

    def get_volume2(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume2)

    def get_volume3(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume3)
