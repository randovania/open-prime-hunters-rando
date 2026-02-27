from open_prime_hunters_rando.common import Vec3
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemy_spawn import EnemySpawn
from open_prime_hunters_rando.parsing.formats.entities.enum import VolumeTypeCommon


class ShriekBatSpawnField(EnemySpawn):
    def get_volume0(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume0)

    @property
    def path_vector(self) -> Vec3:
        return self._raw.data.path_vector

    @path_vector.setter
    def path_vector(self, value: Vec3) -> None:
        self._raw.data.path_vector = value

    def get_volume1(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume1)

    def get_volume2(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume2)
