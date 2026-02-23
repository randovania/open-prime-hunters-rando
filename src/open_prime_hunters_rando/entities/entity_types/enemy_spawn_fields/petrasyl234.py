from open_prime_hunters_rando.common import Vec3
from open_prime_hunters_rando.entities.entity_types.enemy_spawn import EnemySpawn
from open_prime_hunters_rando.entities.enum import VolumeType


class Petrasyl234SpawnField(EnemySpawn):
    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.data.volume0)

    @property
    def position(self) -> Vec3:
        return self._raw.data.position

    @position.setter
    def position(self, value: Vec3) -> None:
        self._raw.data.position = value

    @property
    def weave_offset(self) -> int:
        return self._raw.data.weave_offset

    @weave_offset.setter
    def weave_offset(self, value: int) -> None:
        self._raw.data.weave_offset = value

    @property
    def field(self) -> int:
        return self._raw.data.field

    @field.setter
    def field(self, value: int) -> None:
        self._raw.data.field = value
