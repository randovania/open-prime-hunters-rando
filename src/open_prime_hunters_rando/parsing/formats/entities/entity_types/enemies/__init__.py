from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.carnivorous_plant import CarnivorousPlant
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.common_enemy1_slench import (
    CommonEnemy1Slench,
)
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.common_enemy2_fire_spawn import (
    CommonEnemy2FireSpawn,
)
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.cretaphid_greater_ithrak import (
    CretaphidGreaterIthrak,
)
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields, EnemyType
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.gorea1 import Gorea1
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.gorea2 import Gorea2
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.hunter import Hunter
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.petrasyl234 import Petrasyl234
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.shriek_bat import ShriekBat
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.slench_turret import SlenchTurret
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.temroid_petrasyl1 import TemroidPetrasyl1
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.war_wasp import BarbedWarWasp, WarWasp

__all__ = [
    "CarnivorousPlant",
    "CommonEnemy1Slench",
    "CommonEnemy2FireSpawn",
    "CretaphidGreaterIthrak",
    "Gorea1",
    "Gorea2",
    "Hunter",
    "Petrasyl234",
    "ShriekBat",
    "SlenchTurret",
    "TemroidPetrasyl1",
    "WarWasp",
    "BarbedWarWasp",
    "enemy_type_to_class",
    "enemy_type_to_construct",
]

enemy_type_to_class: dict[EnemyType, type[EnemyFields]] = {
    EnemyType.ZOOMER: CommonEnemy1Slench,
    EnemyType.GEEMER: CommonEnemy1Slench,
    EnemyType.BLASTCAP: CommonEnemy1Slench,
    EnemyType.QUADTROID: CommonEnemy1Slench,
    EnemyType.CRASH_PILLAR: CommonEnemy1Slench,
    EnemyType.SLENCH: CommonEnemy1Slench,
    EnemyType.LESSER_ITHRAK: CommonEnemy1Slench,
    EnemyType.TROCRA: CommonEnemy1Slench,
    EnemyType.VOLDRUM2: CommonEnemy1Slench,
    EnemyType.WAR_WASP: WarWasp,
    EnemyType.SHRIEKBAT: ShriekBat,
    EnemyType.TEMROID: TemroidPetrasyl1,
    EnemyType.PETRASYL1: TemroidPetrasyl1,
    EnemyType.PETRASYL2: Petrasyl234,
    EnemyType.PETRASYL3: Petrasyl234,
    EnemyType.PETRASYL4: Petrasyl234,
    EnemyType.CRETAPHID: CretaphidGreaterIthrak,
    EnemyType.GREATER_ITHRAK: CretaphidGreaterIthrak,
    EnemyType.ALIMBIC_TURRET: CommonEnemy2FireSpawn,
    EnemyType.PSYCHO_BIT1: CommonEnemy2FireSpawn,
    EnemyType.PSYCHO_BIT2: CommonEnemy2FireSpawn,
    EnemyType.VOLDRUM1: CommonEnemy2FireSpawn,
    EnemyType.FIRE_SPAWN: CommonEnemy2FireSpawn,
    EnemyType.CARNIVOROUS_PLANT: CarnivorousPlant,
    EnemyType.BARBED_WAR_WASP: BarbedWarWasp,
    EnemyType.HUNTER: Hunter,
    EnemyType.SLENCH_TURRET: SlenchTurret,
    EnemyType.GOREA1_A: Gorea1,
    EnemyType.GOREA2: Gorea2,
}

enemy_type_to_construct = {etype: eclass.type_construct() for etype, eclass in enemy_type_to_class.items()}
