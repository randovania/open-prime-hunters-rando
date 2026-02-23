from construct import Container

from open_prime_hunters_rando.entities.entity_type import Entity

# from open_prime_hunters_rando.entities.entity_types.enemy_spawn_fields.carnivorous_plant import (
#     CarnivorousPlantSpawnField,
# )
# from open_prime_hunters_rando.entities.entity_types.enemy_spawn_fields.common_enemy1_slench import (
#     CommonEnemy1SlenchSpawnField,
# )
# from open_prime_hunters_rando.entities.entity_types.enemy_spawn_fields.common_enemy2_fire_spawn import (
#     CommonEnemy2FireSpawnSpawnField,
# )
# from open_prime_hunters_rando.entities.entity_types.enemy_spawn_fields.cretaphid_greater_ithrak import (
#     CreatphidGreaterIthrakSpawnField,
# )
# from open_prime_hunters_rando.entities.entity_types.enemy_spawn_fields.gorea1 import Gorea1SpawnField
# from open_prime_hunters_rando.entities.entity_types.enemy_spawn_fields.gorea2 import Gorea2SpawnField
# from open_prime_hunters_rando.entities.entity_types.enemy_spawn_fields.hunter import HunterSpawnField
# from open_prime_hunters_rando.entities.entity_types.enemy_spawn_fields.petrasyl234 import Petrasyl234SpawnField
# from open_prime_hunters_rando.entities.entity_types.enemy_spawn_fields.shriek_bat import ShriekBatSpawnField
# from open_prime_hunters_rando.entities.entity_types.enemy_spawn_fields.slench_turret import SlenchTurretSpawnField
# from open_prime_hunters_rando.entities.entity_types.enemy_spawn_fields.temroid_petrasyl1 import (
#     TemroidPetrsyl1SpawnField,
# )
# from open_prime_hunters_rando.entities.entity_types.enemy_spawn_fields.war_wasp import (
#     BarbedWarWaspSpawnField,
#     WarWaspSpawnField,
# )
from open_prime_hunters_rando.entities.enum import EnemyType, ItemType, Message

# enemy_spawn_field_to_class = {
#     EnemyType.ZOOMER: CommonEnemy1SlenchSpawnField,
#     EnemyType.GEEMER: CommonEnemy1SlenchSpawnField,
#     EnemyType.BLASTCAP: CommonEnemy1SlenchSpawnField,
#     EnemyType.QUADTROID: CommonEnemy1SlenchSpawnField,
#     EnemyType.CRASH_PILLAR: CommonEnemy1SlenchSpawnField,
#     EnemyType.SLENCH: CommonEnemy1SlenchSpawnField,
#     EnemyType.LESSER_ITHRAK: CommonEnemy1SlenchSpawnField,
#     EnemyType.TROCRA: CommonEnemy1SlenchSpawnField,
#     EnemyType.VOLDRUM2: CommonEnemy1SlenchSpawnField,
#     EnemyType.WAR_WASP: WarWaspSpawnField,
#     EnemyType.SHRIEKBAT: ShriekBatSpawnField,
#     EnemyType.TEMROID: TemroidPetrsyl1SpawnField,
#     EnemyType.PETRASYL1: TemroidPetrsyl1SpawnField,
#     EnemyType.PETRASYL2: Petrasyl234SpawnField,
#     EnemyType.PETRASYL3: Petrasyl234SpawnField,
#     EnemyType.PETRASYL4: Petrasyl234SpawnField,
#     EnemyType.CRETAPHID: CreatphidGreaterIthrakSpawnField,
#     EnemyType.GREATER_ITHRAK: CreatphidGreaterIthrakSpawnField,
#     EnemyType.ALIMBIC_TURRET: CommonEnemy2FireSpawnSpawnField,
#     EnemyType.PSYCHO_BIT1: CommonEnemy2FireSpawnSpawnField,
#     EnemyType.PSYCHO_BIT2: CommonEnemy2FireSpawnSpawnField,
#     EnemyType.VOLDRUM1: CommonEnemy2FireSpawnSpawnField,
#     EnemyType.FIRE_SPAWN: CommonEnemy2FireSpawnSpawnField,
#     EnemyType.CARNIVOROUS_PLANT: CarnivorousPlantSpawnField,
#     EnemyType.BARBED_WAR_WASP: BarbedWarWaspSpawnField,
#     EnemyType.HUNTER: HunterSpawnField,
#     EnemyType.SLENCH_TURRET: SlenchTurretSpawnField,
#     EnemyType.GOREA1_A: Gorea1SpawnField,
#     EnemyType.GOREA2: Gorea2SpawnField,
# }


class EnemySpawn(Entity):
    @property
    def enemy_type(self) -> EnemyType:
        return self._raw.data.enemy_type

    @enemy_type.setter
    def enemy_type(self, value: EnemyType) -> None:
        self._raw.data.enemy_type = value

    @property
    def fields(self) -> Container:
        return self._raw.data.fields

    @fields.setter
    def fields(self, value: Container) -> None:
        self._raw.data.fields = value

    @property
    def linked_entity_id(self) -> int:
        return self._raw.data.linked_entity_id

    @linked_entity_id.setter
    def linked_entity_id(self, value: int) -> None:
        self._raw.data.linked_entity_id = value

    @property
    def spawn_limit(self) -> int:
        return self._raw.data.spawn_limit

    @spawn_limit.setter
    def spawn_limit(self, value: int) -> None:
        self._raw.data.spawn_limit = value

    @property
    def spawn_total(self) -> int:
        return self._raw.data.spawn_total

    @spawn_total.setter
    def spawn_total(self, value: int) -> None:
        self._raw.data.spawn_total = value

    @property
    def spawn_count(self) -> int:
        return self._raw.data.spawn_count

    @spawn_count.setter
    def spawn_count(self, value: int) -> None:
        self._raw.data.spawn_count = value

    @property
    def active(self) -> bool:
        return self._raw.data.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.data.active = value

    @property
    def always_active(self) -> bool:
        return self._raw.data.always_active

    @always_active.setter
    def always_active(self, value: bool) -> None:
        self._raw.data.always_active = value

    @property
    def item_chance(self) -> int:
        return self._raw.data.item_chance

    @item_chance.setter
    def item_chance(self, value: int) -> None:
        self._raw.data.item_chance = value

    @property
    def spawner_health(self) -> int:
        return self._raw.data.spawner_health

    @spawner_health.setter
    def spawner_health(self, value: int) -> None:
        self._raw.data.spawner_health = value

    @property
    def cooldown_time(self) -> int:
        return self._raw.data.cooldown_time

    @cooldown_time.setter
    def cooldown_time(self, value: int) -> None:
        self._raw.data.cooldown_time = value

    @property
    def initial_cooldown(self) -> int:
        return self._raw.data.initial_cooldown

    @initial_cooldown.setter
    def initial_cooldown(self, value: int) -> None:
        self._raw.data.initial_cooldown = value

    @property
    def active_distance(self) -> float:
        return self._raw.data.active_distance

    @active_distance.setter
    def active_distance(self, value: float) -> None:
        self._raw.data.active_distance = value

    @property
    def enemy_active_distance(self) -> float:
        return self._raw.data.enemy_active_distance

    @enemy_active_distance.setter
    def enemy_active_distance(self, value: float) -> None:
        self._raw.data.enemy_active_distance = value

    @property
    def node_name(self) -> str:
        return self._raw.data.node_name

    @node_name.setter
    def node_name(self, value: str) -> None:
        self._raw.data.node_name = value

    @property
    def entity_id1(self) -> int:
        return self._raw.data.entity_id1

    @entity_id1.setter
    def entity_id1(self, value: int) -> None:
        self._raw.data.entity_id1 = value

    @property
    def message1(self) -> Message:
        return self._raw.data.message1

    @message1.setter
    def message1(self, value: Message) -> None:
        self._raw.data.message1 = value

    @property
    def entity_id2(self) -> int:
        return self._raw.data.entity_id2

    @entity_id2.setter
    def entity_id2(self, value: int) -> None:
        self._raw.data.entity_id2 = value

    @property
    def message2(self) -> Message:
        return self._raw.data.message2

    @message2.setter
    def message2(self, value: Message) -> None:
        self._raw.data.message2 = value

    @property
    def entity_id3(self) -> int:
        return self._raw.data.entity_id3

    @entity_id3.setter
    def entity_id3(self, value: int) -> None:
        self._raw.data.entity_id3 = value

    @property
    def message3(self) -> Message:
        return self._raw.data.message3

    @message3.setter
    def message3(self, value: Message) -> None:
        self._raw.data.message3 = value

    @property
    def item_type(self) -> ItemType:
        return self._raw.data.item_type

    @item_type.setter
    def item_type(self, value: ItemType) -> None:
        self._raw.data.item_type = value
