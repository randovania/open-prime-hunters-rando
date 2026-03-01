import enum

import construct
from construct import (
    Byte,
    Construct,
    Flag,
    Int16sl,
    Int16ul,
    Padded,
    Struct,
    Switch,
)

from open_prime_hunters_rando.parsing.common_types import DecodedString, FixedPoint, ItemTypeConstruct, MessageConstruct
from open_prime_hunters_rando.parsing.construct_extensions import EnumAdapter
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.carnivorous_plant import (
    CarnvirousPlantEntityData,
)
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.common_enemy1_slench import (
    CommonEnemy1SlenchEntityData,
)
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.common_enemy2_fire_spawn import (
    CommonEnemy2FireSpawnEntityData,
)
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.cretaphid_greater_ithrak import (
    CretaphidGreaterIthrakEntityData,
)
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.gorea1 import Gorea1EntityData
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.gorea2 import Gorea2EntityData
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.hunter import HunterEntityData
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.petrasyl234 import Petrasyl234EntityData
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.shriek_bat import ShriekBatEntityData
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.slench_turret import SlenchTurretEntityData
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.temroid_petrasyl1 import (
    TemroidPetrasyllEntityData,
)
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.war_wasp import (
    BarbedWarWaspEntityData,
    WarWaspEntityData,
)
from open_prime_hunters_rando.parsing.formats.entities.enum import ItemType, Message


class EnemyType(enum.Enum):
    WAR_WASP = 0
    ZOOMER = 1
    TEMROID = 2
    PETRASYL1 = 3
    PETRASYL2 = 4
    PETRASYL3 = 5
    PETRASYL4 = 6
    UNKNOWN_7 = 7  # unused
    UNKNOWN_8 = 8  # unused
    UNKNOWN_9 = 9  # unused
    BARBED_WAR_WASP = 10
    SHRIEKBAT = 11
    GEEMER = 12
    UNKNOWN_13 = 13  # unused
    UNKNOWN_14 = 14  # unused
    UNKNOWN_15 = 15  # unused
    BLASTCAP = 16
    UNKNOWN_17 = 17  # unused
    ALIMBIC_TURRET = 18
    CRETAPHID = 19
    CRETAPHID_EYE = 20
    CRETAPHID_CRYSTAL = 21
    UNKNOWN_22 = 22  # unused (Cretaphid-related)
    PSYCHO_BIT1 = 23
    GOREA1_A = 24
    GOREA_HEAD = 25
    GOREA_ARM = 26
    GOREA_LEG = 27
    GOREA1_B = 28
    GOREA_SEAL_SPHERE1 = 29
    TROCRA = 30
    GOREA2 = 31
    GOREA_SEAL_SPHERE2 = 32
    GOREA_METEOR = 33
    PSYCHO_BIT2 = 34  # unused
    VOLDRUM2 = 35
    VOLDRUM1 = 36
    QUADTROID = 37
    CRASH_PILLAR = 38
    FIRE_SPAWN = 39
    SPAWNER = 40
    SLENCH = 41
    SLENCH_SHIELD = 42
    SLENCH_NEST = 43
    SLENCH_SYNAPSE = 44
    SLENCH_TURRET = 45
    LESSER_ITHRAK = 46
    GREATER_ITHRAK = 47
    HUNTER = 48
    FORCE_FIELD_LOCK = 49
    HIT_ZONE = 50  # used by 39/46/47
    CARNIVOROUS_PLANT = 51


EnemyTypeConstruct = EnumAdapter(EnemyType, Byte)

enemy_type_to_entity_data = {
    EnemyType.ZOOMER: CommonEnemy1SlenchEntityData,
    EnemyType.GEEMER: CommonEnemy1SlenchEntityData,
    EnemyType.BLASTCAP: CommonEnemy1SlenchEntityData,
    EnemyType.QUADTROID: CommonEnemy1SlenchEntityData,
    EnemyType.CRASH_PILLAR: CommonEnemy1SlenchEntityData,
    EnemyType.SLENCH: CommonEnemy1SlenchEntityData,
    EnemyType.LESSER_ITHRAK: CommonEnemy1SlenchEntityData,
    EnemyType.TROCRA: CommonEnemy1SlenchEntityData,
    EnemyType.VOLDRUM2: CommonEnemy1SlenchEntityData,
    EnemyType.WAR_WASP: WarWaspEntityData,
    EnemyType.SHRIEKBAT: ShriekBatEntityData,
    EnemyType.TEMROID: TemroidPetrasyllEntityData,
    EnemyType.PETRASYL1: TemroidPetrasyllEntityData,
    EnemyType.PETRASYL2: Petrasyl234EntityData,
    EnemyType.PETRASYL3: Petrasyl234EntityData,
    EnemyType.PETRASYL4: Petrasyl234EntityData,
    EnemyType.CRETAPHID: CretaphidGreaterIthrakEntityData,
    EnemyType.GREATER_ITHRAK: CretaphidGreaterIthrakEntityData,
    EnemyType.ALIMBIC_TURRET: CommonEnemy2FireSpawnEntityData,
    EnemyType.PSYCHO_BIT1: CommonEnemy2FireSpawnEntityData,
    EnemyType.PSYCHO_BIT2: CommonEnemy2FireSpawnEntityData,
    EnemyType.VOLDRUM1: CommonEnemy2FireSpawnEntityData,
    EnemyType.FIRE_SPAWN: CommonEnemy2FireSpawnEntityData,
    EnemyType.CARNIVOROUS_PLANT: CarnvirousPlantEntityData,
    EnemyType.BARBED_WAR_WASP: BarbedWarWaspEntityData,
    EnemyType.HUNTER: HunterEntityData,
    EnemyType.SLENCH_TURRET: SlenchTurretEntityData,
    EnemyType.GOREA1_A: Gorea1EntityData,
    EnemyType.GOREA2: Gorea2EntityData,
}
EnemySpawnEntityData = Struct(
    "enemy_type" / Padded(4, EnemyTypeConstruct),
    "fields" / Padded(400, Switch(construct.this.enemy_type, enemy_type_to_entity_data)),
    "linked_entity_id" / Int16sl,
    "spawn_limit" / Byte,
    "spawn_total" / Byte,
    "spawn_count" / Byte,
    "active" / Flag,
    "always_active" / Flag,
    "item_chance" / Byte,
    "spawner_health" / Int16ul,
    "cooldown_time" / Int16ul,
    "initial_cooldown" / Padded(4, Int16ul),
    "active_distance" / FixedPoint,
    "enemy_active_distance" / FixedPoint,
    "node_name" / DecodedString,
    "entity_id1" / Padded(4, Int16sl),
    "message1" / MessageConstruct,
    "entity_id2" / Padded(4, Int16sl),
    "message2" / MessageConstruct,
    "entity_id3" / Padded(4, Int16sl),
    "message3" / MessageConstruct,
    "item_type" / ItemTypeConstruct,
)


# class EnemyFields(Adapter):
#     def __init__(self):
#         super().__init__(EnemySpawnEntityData)

#     def _decode(self, obj: Container, context: Container, path: str) -> EnemyType:
#         match obj.enemy_type:
#             case EnemyType.ZOOMER:
#                 cls = CommonEnemy1SlenchSpawnField

#         return cls(obj)

#     def _encode(self, obj: EnemyType, context: Container, path: str) -> Container:
#         return obj._raw


class BaseEnemySpawn(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return EnemySpawnEntityData

    enemy_type = field(EnemyType)

    fields = field()  # FIXME: Needs updating like volume.py I think

    linked_entity_id = field(int)

    spawn_limit = field(int)
    spawn_total = field(int)
    spawn_count = field(int)

    active = field(bool)
    always_active = field(bool)

    item_chance = field(int)

    spawner_health = field(int)

    cooldown_time = field(int)
    initial_cooldown = field(int)

    active_distance = field(float)
    enemy_active_distance = field(float)

    node_name = field(str)

    entity_id1 = field(int)
    message1 = field(Message)

    entity_id2 = field(int)
    message2 = field(Message)

    entity_id3 = field(int)
    message3 = field(Message)

    item_type = field(ItemType)
