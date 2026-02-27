from open_prime_hunters_rando.common import Vec3
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemy_spawn import EnemySpawn


class Gorea2SpawnField(EnemySpawn):
    @property
    def field1(self) -> Vec3:
        return self._raw.data.field1

    @field1.setter
    def field1(self, value: Vec3) -> None:
        self._raw.data.field1 = value

    @property
    def field2(self) -> int:
        return self._raw.data.field2

    @field2.setter
    def field2(self, value: int) -> None:
        self._raw.data.field2 = value

    @property
    def field3(self) -> int:
        return self._raw.data.field3

    @field3.setter
    def field3(self, value: int) -> None:
        self._raw.data.field3 = value
