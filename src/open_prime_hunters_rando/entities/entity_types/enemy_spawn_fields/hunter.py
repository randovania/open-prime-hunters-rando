import enum

from open_prime_hunters_rando.entities.entity_types.enemy_spawn import EnemySpawn


class Hunter(enum.Enum):
    SAMUS = 0
    KANDEN = 1
    TRACE = 2
    SYLUX = 3
    NOXUS = 4
    SPIRE = 5
    WEAVEL = 6
    GUARDIAN = 7
    RANDOM = 8


class HunterSpawnField(EnemySpawn):
    @property
    def hunter_id(self) -> Hunter:
        return self._raw.data.hunter_id

    @hunter_id.setter
    def hunter_id(self, value: Hunter) -> None:
        self._raw.data.hunter_id = value

    @property
    def encounter_type(self) -> int:
        return self._raw.data.encounter_type

    @encounter_type.setter
    def encounter_type(self, value: int) -> None:
        self._raw.data.encounter_type = value

    @property
    def hunter_weapon(self) -> int:
        return self._raw.data.hunter_weapon

    @hunter_weapon.setter
    def hunter_weapon(self, value: int) -> None:
        self._raw.data.hunter_weapon = value

    @property
    def hunter_health(self) -> int:
        return self._raw.data.hunter_health

    @hunter_health.setter
    def hunter_health(self, value: int) -> None:
        self._raw.data.hunter_health = value

    @property
    def hunter_health_max(self) -> int:
        return self._raw.data.hunter_health_max

    @hunter_health_max.setter
    def hunter_health_max(self, value: int) -> None:
        self._raw.data.hunter_health_max = value

    @property
    def field(self) -> int:
        return self._raw.data.field

    @field.setter
    def field(self, value: int) -> None:
        self._raw.data.field = value

    @property
    def hunter_color(self) -> int:
        return self._raw.data.hunter_color

    @hunter_color.setter
    def hunter_color(self, value: int) -> None:
        self._raw.data.hunter_color = value

    @property
    def hunter_chance(self) -> int:
        return self._raw.data.hunter_chance

    @hunter_chance.setter
    def hunter_chance(self, value: int) -> None:
        self._raw.data.hunter_chance = value
