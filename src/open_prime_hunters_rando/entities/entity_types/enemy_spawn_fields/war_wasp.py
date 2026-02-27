from open_prime_hunters_rando.common import Vec3
from open_prime_hunters_rando.entities.entity_types.enemy_spawn import EnemySpawn
from open_prime_hunters_rando.entities.enum import VolumeTypeCommon


class WarWaspSpawnField(EnemySpawn):
    def get_volume0(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume0)

    def get_volume1(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume1)

    def get_volume2(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume2)

    @property
    def movement_vectors(self) -> list[Vec3]:
        return self._raw.data.movement_vectors

    @movement_vectors.setter
    def movement_vectors(self, value: list[Vec3]) -> None:
        self._raw.data.movement_vectors = value

    @property
    def position_count(self) -> int:
        return self._raw.data.position_count

    @position_count.setter
    def position_count(self, value: int) -> None:
        self._raw.data.position_count = value

    @property
    def movement_type(self) -> int:
        return self._raw.data.movement_type

    @movement_type.setter
    def movement_type(self, value: int) -> None:
        self._raw.data.movement_type = value


class BarbedWarWaspSpawnField(WarWaspSpawnField):
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
