from construct import Container

from open_prime_hunters_rando.constants import Vec3
from open_prime_hunters_rando.entities.enum import EnemyType, Hunter, ItemType, Message, VolumeType


class WarWaspData:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.volume0)

    def get_volume1(self) -> VolumeType:
        return VolumeType(self._raw.volume1)

    def get_volume2(self) -> VolumeType:
        return VolumeType(self._raw.volume2)

    @property
    def movement_vectors(self) -> list[Vec3]:
        return self._raw.movement_vectors

    @movement_vectors.setter
    def movement_vectors(self, value: list[Vec3]) -> None:
        self._raw.movement_vectors = value

    @property
    def position_count(self) -> int:
        return self._raw.position_count

    @position_count.setter
    def position_count(self, value: int) -> None:
        self._raw.position_count = value

    @property
    def movement_type(self) -> int:
        return self._raw.movement_type

    @movement_type.setter
    def movement_type(self, value: int) -> None:
        self._raw.movement_type = value


class CommonEnemy1SlenchSpawnField:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.volume0)

    def get_volume1(self) -> VolumeType:
        return VolumeType(self._raw.volume1)

    def get_volume2(self) -> VolumeType:
        return VolumeType(self._raw.volume2)

    def get_volume3(self) -> VolumeType:
        return VolumeType(self._raw.volume3)


class WarWaspSpawnField:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def war_wasp(self) -> WarWaspData:
        return self._raw.war_wasp

    def get_war_wasp(self) -> WarWaspData:
        return WarWaspData(self._raw.war_wasp)


class ShriekBatSpawnField:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.volume0)

    @property
    def path_vector(self) -> Vec3:
        return self._raw.path_vector

    @path_vector.setter
    def path_vector(self, value: Vec3) -> None:
        self._raw.path_vector = value

    def get_volume1(self) -> VolumeType:
        return VolumeType(self._raw.volume1)

    def get_volume2(self) -> VolumeType:
        return VolumeType(self._raw.volume2)


class TemroidPetrsyl1SpawnField:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.volume0)

    @property
    def facing(self) -> Vec3:
        return self._raw.facing

    @facing.setter
    def facing(self, value: Vec3) -> None:
        self._raw.facing = value

    @property
    def position(self) -> Vec3:
        return self._raw.position

    @position.setter
    def position(self, value: Vec3) -> None:
        self._raw.position = value

    @property
    def idle_range(self) -> Vec3:
        return self._raw.idle_range

    @idle_range.setter
    def idle_range(self, value: Vec3) -> None:
        self._raw.idle_range = value


class Petrasyl234SpawnField:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.volume0)

    @property
    def position(self) -> Vec3:
        return self._raw.position

    @position.setter
    def position(self, value: Vec3) -> None:
        self._raw.position = value

    @property
    def weave_offset(self) -> int:
        return self._raw.weave_offset

    @weave_offset.setter
    def weave_offset(self, value: int) -> None:
        self._raw.weave_offset = value

    @property
    def field(self) -> int:
        return self._raw.field

    @field.setter
    def field(self, value: int) -> None:
        self._raw.field = value


class CreatphidGreaterIthrakSpawnField:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def enemy_subtype(self) -> int:
        return self._raw.enemy_subtype

    @enemy_subtype.setter
    def enemy_subtype(self, value: int) -> None:
        self._raw.enemy_subtype = value

    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.volume0)

    def get_volume1(self) -> VolumeType:
        return VolumeType(self._raw.volume1)

    def get_volume2(self) -> VolumeType:
        return VolumeType(self._raw.volume2)

    def get_volume3(self) -> VolumeType:
        return VolumeType(self._raw.volume3)


class CommonEnemy2FireSpawnSpawnField:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def enemy_subtype(self) -> int:
        return self._raw.enemy_subtype

    @enemy_subtype.setter
    def enemy_subtype(self, value: int) -> None:
        self._raw.enemy_subtype = value

    @property
    def enemy_version(self) -> int:
        return self._raw.enemy_version

    @enemy_version.setter
    def enemy_version(self, value: int) -> None:
        self._raw.enemy_version = value

    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.volume0)

    def get_volume1(self) -> VolumeType:
        return VolumeType(self._raw.volume1)

    def get_volume2(self) -> VolumeType:
        return VolumeType(self._raw.volume2)

    def get_volume3(self) -> VolumeType:
        return VolumeType(self._raw.volume3)


class CarnivorousPlantSpawnField:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def enemy_health(self) -> int:
        return self._raw.enemy_health

    @enemy_health.setter
    def enemy_health(self, value: int) -> None:
        self._raw.enemy_health = value

    @property
    def enemy_damage(self) -> int:
        return self._raw.enemy_damage

    @enemy_damage.setter
    def enemy_damage(self, value: int) -> None:
        self._raw.enemy_damage = value

    @property
    def enemy_subtype(self) -> int:
        return self._raw.enemy_subtype

    @enemy_subtype.setter
    def enemy_subtype(self, value: int) -> None:
        self._raw.enemy_subtype = value

    def war_wasp(self) -> WarWaspData:
        return self._raw.war_wasp

    def get_war_wasp(self) -> WarWaspData:
        return WarWaspData(self._raw.war_wasp)


class BarbedWarWaspSpawnField:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def enemy_subtype(self) -> int:
        return self._raw.enemy_subtype

    @enemy_subtype.setter
    def enemy_subtype(self, value: int) -> None:
        self._raw.enemy_subtype = value

    @property
    def enemy_version(self) -> int:
        return self._raw.enemy_version

    @enemy_version.setter
    def enemy_version(self, value: int) -> None:
        self._raw.enemy_version = value

    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.volume0)


class HunterSpawnField:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def hunter_id(self) -> Hunter:
        return self._raw.hunter_id

    @hunter_id.setter
    def hunter_id(self, value: Hunter) -> None:
        self._raw.hunter_id = value

    @property
    def encounter_type(self) -> int:
        return self._raw.encounter_type

    @encounter_type.setter
    def encounter_type(self, value: int) -> None:
        self._raw.encounter_type = value

    @property
    def hunter_weapon(self) -> int:
        return self._raw.hunter_weapon

    @hunter_weapon.setter
    def hunter_weapon(self, value: int) -> None:
        self._raw.hunter_weapon = value

    @property
    def hunter_health(self) -> int:
        return self._raw.hunter_health

    @hunter_health.setter
    def hunter_health(self, value: int) -> None:
        self._raw.hunter_health = value

    @property
    def hunter_health_max(self) -> int:
        return self._raw.hunter_health_max

    @hunter_health_max.setter
    def hunter_health_max(self, value: int) -> None:
        self._raw.hunter_health_max = value

    @property
    def field(self) -> int:
        return self._raw.field

    @field.setter
    def field(self, value: int) -> None:
        self._raw.field = value

    @property
    def hunter_color(self) -> int:
        return self._raw.hunter_color

    @hunter_color.setter
    def hunter_color(self, value: int) -> None:
        self._raw.hunter_color = value

    @property
    def hunter_chance(self) -> int:
        return self._raw.hunter_chance

    @hunter_chance.setter
    def hunter_chance(self, value: int) -> None:
        self._raw.hunter_chance = value


class SlenchTurretSpawnField:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def enemy_subtype(self) -> int:
        return self._raw.enemy_subtype

    @enemy_subtype.setter
    def enemy_subtype(self, value: int) -> None:
        self._raw.enemy_subtype = value

    @property
    def enemy_version(self) -> int:
        return self._raw.enemy_version

    @enemy_version.setter
    def enemy_version(self, value: int) -> None:
        self._raw.enemy_version = value

    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.volume0)

    def get_volume1(self) -> VolumeType:
        return VolumeType(self._raw.volume1)

    @property
    def index(self) -> int:
        return self._raw.index

    @index.setter
    def index(self, value: int) -> None:
        self._raw.index = value


class Gorea1SpawnField:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def sphere1_position(self) -> Vec3:
        return self._raw.sphere1_position

    @sphere1_position.setter
    def sphere1_position(self, value: Vec3) -> None:
        self._raw.sphere1_position = value

    @property
    def sphere1_radius(self) -> float:
        return self._raw.sphere1_radius

    @sphere1_radius.setter
    def sphere1_radius(self, value: float) -> None:
        self._raw.sphere1_radius = value

    @property
    def sphere2_position(self) -> Vec3:
        return self._raw.sphere2_position

    @sphere2_position.setter
    def sphere2_position(self, value: Vec3) -> None:
        self._raw.sphere2_position = value

    @property
    def sphere2_radius(self) -> float:
        return self._raw.sphere2_radiusfield3

    @sphere2_radius.setter
    def sphere2_radius(self, value: float) -> None:
        self._raw.sphere2_radius = value


class Gorea2SpawnField:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def field1(self) -> Vec3:
        return self._raw.field1

    @field1.setter
    def field1(self, value: Vec3) -> None:
        self._raw.field1 = value

    @property
    def field2(self) -> int:
        return self._raw.field2

    @field2.setter
    def field2(self, value: int) -> None:
        self._raw.field2 = value

    @property
    def field3(self) -> int:
        return self._raw.field3

    @field3.setter
    def field3(self, value: int) -> None:
        self._raw.field3 = value


class EnemySpawn:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def enemy_type(self) -> EnemyType:
        return self._raw.enemy_type

    @enemy_type.setter
    def enemy_type(self, value: EnemyType) -> None:
        self._raw.enemy_type = value

    def fields(self) -> Container:
        return self._raw.fields

    def common_enemy1_slench_spawn_field(self) -> CommonEnemy1SlenchSpawnField:
        return CommonEnemy1SlenchSpawnField(self._raw.fields)

    def war_wasp_spawn_field(self) -> WarWaspSpawnField:
        return WarWaspSpawnField(self._raw.fields)

    def shriekbat_spawn_field(self) -> ShriekBatSpawnField:
        return ShriekBatSpawnField(self._raw.fields)

    def temroid_petrasyl1_spawn_field(self) -> TemroidPetrsyl1SpawnField:
        return TemroidPetrsyl1SpawnField(self._raw.fields)

    def petrasyl234_spawn_field(self) -> Petrasyl234SpawnField:
        return Petrasyl234SpawnField(self._raw.fields)

    def cretaphid_greater_ithrak_spawn_field(self) -> CreatphidGreaterIthrakSpawnField:
        return CreatphidGreaterIthrakSpawnField(self._raw.fields)

    def common_enemy2_fire_spawn_spawn_field(self) -> CommonEnemy2FireSpawnSpawnField:
        return CommonEnemy2FireSpawnSpawnField(self._raw.fields)

    def carnivorous_plant_spawn_field(self) -> CarnivorousPlantSpawnField:
        return CarnivorousPlantSpawnField(self._raw.fields)

    def barbed_war_wasp_spawn_field(self) -> BarbedWarWaspSpawnField:
        return BarbedWarWaspSpawnField(self._raw.fields)

    def hunter_spawn_field(self) -> HunterSpawnField:
        return HunterSpawnField(self._raw.fields)

    def slench_turret_spawn_field(self) -> SlenchTurretSpawnField:
        return SlenchTurretSpawnField(self._raw.fields)

    def gorea1_spawn_field(self) -> Gorea1SpawnField:
        return Gorea1SpawnField(self._raw.fields)

    def gorea2_spawn_field(self) -> Gorea2SpawnField:
        return Gorea2SpawnField(self._raw.fields)

    @property
    def linked_entity_id(self) -> int:
        return self._raw.linked_entity_id

    @linked_entity_id.setter
    def linked_entity_id(self, value: int) -> None:
        self._raw.linked_entity_id = value

    @property
    def spawn_limit(self) -> int:
        return self._raw.spawn_limit

    @spawn_limit.setter
    def spawn_limit(self, value: int) -> None:
        self._raw.spawn_limit = value

    @property
    def spawn_total(self) -> int:
        return self._raw.spawn_total

    @spawn_total.setter
    def spawn_total(self, value: int) -> None:
        self._raw.spawn_total = value

    @property
    def spawn_count(self) -> int:
        return self._raw.spawn_count

    @spawn_count.setter
    def spawn_count(self, value: int) -> None:
        self._raw.spawn_count = value

    @property
    def active(self) -> bool:
        return self._raw.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.active = value

    @property
    def always_active(self) -> bool:
        return self._raw.always_active

    @always_active.setter
    def always_active(self, value: bool) -> None:
        self._raw.always_active = value

    @property
    def item_chance(self) -> int:
        return self._raw.item_chance

    @item_chance.setter
    def item_chance(self, value: int) -> None:
        self._raw.item_chance = value

    @property
    def spawner_health(self) -> int:
        return self._raw.spawner_health

    @spawner_health.setter
    def spawner_health(self, value: int) -> None:
        self._raw.spawner_health = value

    @property
    def cooldown_time(self) -> int:
        return self._raw.cooldown_time

    @cooldown_time.setter
    def cooldown_time(self, value: int) -> None:
        self._raw.cooldown_time = value

    @property
    def initial_cooldown(self) -> int:
        return self._raw.initial_cooldown

    @initial_cooldown.setter
    def initial_cooldown(self, value: int) -> None:
        self._raw.initial_cooldown = value

    @property
    def active_distance(self) -> float:
        return self._raw.active_distance

    @active_distance.setter
    def active_distance(self, value: float) -> None:
        self._raw.active_distance = value

    @property
    def enemy_active_distance(self) -> float:
        return self._raw.enemy_active_distance

    @enemy_active_distance.setter
    def enemy_active_distance(self, value: float) -> None:
        self._raw.enemy_active_distance = value

    @property
    def node_name(self) -> str:
        return self._raw.node_name

    @node_name.setter
    def node_name(self, value: str) -> None:
        self._raw.node_name = value

    @property
    def entity_id1(self) -> int:
        return self._raw.entity_id1

    @entity_id1.setter
    def entity_id1(self, value: int) -> None:
        self._raw.entity_id1 = value

    @property
    def message1(self) -> Message:
        return self._raw.message1

    @message1.setter
    def message1(self, value: Message) -> None:
        self._raw.message1 = value

    @property
    def entity_id2(self) -> int:
        return self._raw.entity_id2

    @entity_id2.setter
    def entity_id2(self, value: int) -> None:
        self._raw.entity_id2 = value

    @property
    def message2(self) -> Message:
        return self._raw.message2

    @message2.setter
    def message2(self, value: Message) -> None:
        self._raw.message2 = value

    @property
    def entity_id3(self) -> int:
        return self._raw.entity_id3

    @entity_id3.setter
    def entity_id3(self, value: int) -> None:
        self._raw.entity_id3 = value

    @property
    def message3(self) -> Message:
        return self._raw.message3

    @message3.setter
    def message3(self, value: Message) -> None:
        self._raw.message3 = value

    @property
    def item_type(self) -> ItemType:
        return self._raw.item_type

    @item_type.setter
    def item_type(self, value: ItemType) -> None:
        self._raw.item_type = value
