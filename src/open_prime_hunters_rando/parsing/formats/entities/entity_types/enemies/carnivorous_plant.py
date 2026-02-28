from open_prime_hunters_rando.parsing.common_types.volume import VolumeTypeCommon
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemy_spawn import EnemySpawn


class CarnivorousPlantSpawnField(EnemySpawn):
    @property
    def enemy_health(self) -> int:
        return self._raw.data.enemy_health

    @enemy_health.setter
    def enemy_health(self, value: int) -> None:
        self._raw.data.enemy_health = value

    @property
    def enemy_damage(self) -> int:
        return self._raw.data.enemy_damage

    @enemy_damage.setter
    def enemy_damage(self, value: int) -> None:
        self._raw.data.enemy_damage = value

    @property
    def enemy_subtype(self) -> int:
        return self._raw.data.enemy_subtype

    @enemy_subtype.setter
    def enemy_subtype(self, value: int) -> None:
        self._raw.data.enemy_subtype = value

    def get_volume0(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume0)
