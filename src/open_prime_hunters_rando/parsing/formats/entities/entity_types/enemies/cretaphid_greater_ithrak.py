from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemy_spawn import EnemySpawn
from open_prime_hunters_rando.parsing.formats.entities.enum import VolumeTypeCommon


class CreatphidGreaterIthrakSpawnField(EnemySpawn):
    @property
    def enemy_subtype(self) -> int:
        return self._raw.data.enemy_subtype

    @enemy_subtype.setter
    def enemy_subtype(self, value: int) -> None:
        self._raw.data.enemy_subtype = value

    def get_volume0(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume0)

    def get_volume1(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume1)

    def get_volume2(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume2)

    def get_volume3(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume3)
