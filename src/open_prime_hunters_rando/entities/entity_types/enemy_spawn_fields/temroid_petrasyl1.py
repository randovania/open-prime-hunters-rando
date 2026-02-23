from open_prime_hunters_rando.common import Vec3
from open_prime_hunters_rando.entities.entity_types.enemy_spawn import EnemySpawn
from open_prime_hunters_rando.entities.enum import VolumeType


class TemroidPetrsyl1SpawnField(EnemySpawn):
    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.data.volume0)

    @property
    def facing(self) -> Vec3:
        return self._raw.data.facing

    @facing.setter
    def facing(self, value: Vec3) -> None:
        self._raw.data.facing = value

    @property
    def position(self) -> Vec3:
        return self._raw.data.position

    @position.setter
    def position(self, value: Vec3) -> None:
        self._raw.data.position = value

    @property
    def idle_range(self) -> Vec3:
        return self._raw.data.idle_range

    @idle_range.setter
    def idle_range(self, value: Vec3) -> None:
        self._raw.data.idle_range = value
