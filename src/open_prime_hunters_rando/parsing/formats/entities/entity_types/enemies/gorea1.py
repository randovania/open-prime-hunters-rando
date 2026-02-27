from open_prime_hunters_rando.common import Vec3
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemy_spawn import EnemySpawn


class Gorea1SpawnField(EnemySpawn):
    @property
    def sphere1_position(self) -> Vec3:
        return self._raw.data.sphere1_position

    @sphere1_position.setter
    def sphere1_position(self, value: Vec3) -> None:
        self._raw.data.sphere1_position = value

    @property
    def sphere1_radius(self) -> float:
        return self._raw.data.sphere1_radius

    @sphere1_radius.setter
    def sphere1_radius(self, value: float) -> None:
        self._raw.data.sphere1_radius = value

    @property
    def sphere2_position(self) -> Vec3:
        return self._raw.data.sphere2_position

    @sphere2_position.setter
    def sphere2_position(self, value: Vec3) -> None:
        self._raw.data.sphere2_position = value

    @property
    def sphere2_radius(self) -> float:
        return self._raw.data.sphere2_radiusfield3

    @sphere2_radius.setter
    def sphere2_radius(self, value: float) -> None:
        self._raw.data.sphere2_radius = value
