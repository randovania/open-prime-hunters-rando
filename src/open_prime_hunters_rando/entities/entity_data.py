import dataclasses
from enum import Enum


@dataclasses.dataclass(frozen=True)
class EntityData:
    entity_id: int


class EntityType(Enum):
    ITEM_SPAWN = 4
    ARTIFACT = 17
    FORCE_FIELD = 19


class ItemType(Enum):
    ENERGY_TANK = "EnergyTank"
    VOLT_DRIVER = "VoltDriver"
    MISSILE_EXPANSION = "MissileExpansion"
    BATTLEHAMMER = "Battlehammer"
    IMPERIALIST = "Imperialist"
    JUDICATOR = "Judicator"
    MAGMAUL = "Magmaul"
    SHOCK_COIL = "ShockCoil"
    UA_EXPANSION = "UAExpansion"


@dataclasses.dataclass(frozen=True)
class PickupData(EntityData):
    active: bool = True
    has_base: bool = True


@dataclasses.dataclass(frozen=True)
class ItemSpawnEntityData(PickupData):
    item_type: ItemType = ItemType.MISSILE_EXPANSION
    entity_type: EntityType = EntityType.ITEM_SPAWN
    notify_entity_id: int = 0
    collected_message: int = 0


@dataclasses.dataclass(frozen=True)
class ArtifactEntityData(PickupData):
    entity_type: EntityType = EntityType.ARTIFACT
    message1_target: int = 0
    message1: int = 0
    message2_target: int = 0
    message2: int = 0
    message3_target: int = 0
    message3: int = 0


class ForceFieldType(Enum):
    POWER_BEAM = 0
    VOLT_DRIVER = 1
    MISSILE = 2
    BATTLEHAMMER = 3
    IMPERIALIST = 4
    JUDICATOR = 5
    MAGMAUL = 6
    SHOCK_COIL = 7
    OMEGA_CANNON = 8
    NONE = 9


@dataclasses.dataclass(frozen=True)
class ForceFieldEntityData(EntityData):
    type: ForceFieldType
    entity_type: EntityType = EntityType.FORCE_FIELD
    active: bool = True


@dataclasses.dataclass(frozen=True)
class LevelData:
    room_id: int
    entity_file: str
    entities: list


ALL_ENTITIES_DATA: dict[str, LevelData] = {
    # Alinos
    "Alinos Gateway": LevelData(
        room_id=27,
        entity_file="Unit1_Land",
        entities=[
            ItemSpawnEntityData(
                entity_id=13,
                item_type=ItemType.MISSILE_EXPANSION,
            ),
        ],
    ),
    "Alinos Perch": LevelData(
        room_id=39,
        entity_file="unit1_RM2",
        entities=[
            ItemSpawnEntityData(
                entity_id=15,
                item_type=ItemType.MISSILE_EXPANSION,
            ),
            ForceFieldEntityData(
                entity_id=26,
                type=ForceFieldType.MAGMAUL,
            ),
        ],
    ),
    "Biodefense Chamber 02": LevelData(
        room_id=35,
        entity_file="Unit1_b1",
        entities=[
            ArtifactEntityData(
                entity_id=2,
                message1_target=4,
                message1=16,
            ),
        ],
    ),
    "Biodefense Chamber 06": LevelData(
        room_id=44,
        entity_file="Unit1_b2",
        entities=[
            ArtifactEntityData(
                entity_id=8,
                message1_target=1,
                message1=16,
            ),
        ],
    ),
    "Council Chamber": LevelData(
        room_id=40,
        entity_file="unit1_rm3",
        entities=[
            ItemSpawnEntityData(
                entity_id=5,
                item_type=ItemType.ENERGY_TANK,
            ),
            ItemSpawnEntityData(
                entity_id=21,
                active=False,
                has_base=False,
                item_type=ItemType.MAGMAUL,
            ),
            ArtifactEntityData(
                entity_id=19,
            ),
            ForceFieldEntityData(
                entity_id=22,
                type=ForceFieldType.MAGMAUL,
            ),
            ForceFieldEntityData(
                entity_id=23,
                type=ForceFieldType.MAGMAUL,
            ),
            ForceFieldEntityData(
                entity_id=26,
                type=ForceFieldType.MAGMAUL,
            ),
        ],
    ),
    "Crash Site": LevelData(
        room_id=42,
        entity_file="Unit1_C3",
        entities=[
            ArtifactEntityData(
                entity_id=4,
                has_base=False,
            ),
        ],
    ),
    "Echo Hall": LevelData(
        room_id=28,
        entity_file="Unit1_C0",
        entities=[
            ArtifactEntityData(
                entity_id=3,
            ),
            ItemSpawnEntityData(
                entity_id=15,
                has_base=False,
                item_type=ItemType.ENERGY_TANK,
            ),
        ],
    ),
    "Elder Passage": LevelData(
        room_id=31,
        entity_file="unit_RM6",
        entities=[
            ArtifactEntityData(
                entity_id=4,
                has_base=False,
                message1_target=40,
                message1=9,
                message2_target=1,
                message2=9,
            ),
        ],
    ),
    "High Ground": LevelData(
        room_id=29,
        entity_file="unit1_RM1",
        entities=[
            ItemSpawnEntityData(
                entity_id=80,
                has_base=False,
                item_type=ItemType.MISSILE_EXPANSION,
            ),
            ArtifactEntityData(
                entity_id=24,
                has_base=False,
                message1_target=17,
                message1=16,
                message2_target=56,
                message2=33,
                message3_target=94,
                message3=9,
            ),
            ForceFieldEntityData(
                entity_id=6,
                type=ForceFieldType.VOLT_DRIVER,
            ),
            ForceFieldEntityData(
                entity_id=8,
                type=ForceFieldType.VOLT_DRIVER,
            ),
            ForceFieldEntityData(
                entity_id=9,
                type=ForceFieldType.VOLT_DRIVER,
            ),
            ForceFieldEntityData(
                entity_id=74,
                type=ForceFieldType.JUDICATOR,
            ),
            ForceFieldEntityData(
                entity_id=77,
                type=ForceFieldType.JUDICATOR,
            ),
            ForceFieldEntityData(
                entity_id=40,
                type=ForceFieldType.VOLT_DRIVER,
            ),
        ],
    ),
    "Magma Drop": LevelData(
        room_id=30,
        entity_file="Unit1_C4",
        entities=[
            ItemSpawnEntityData(
                entity_id=14,
                item_type=ItemType.UA_EXPANSION,
            ),
        ],
    ),
    "Piston Cave": LevelData(
        room_id=38,
        entity_file="Unit1_C5",
        entities=[
            ArtifactEntityData(
                entity_id=38,
                has_base=False,
                message1_target=36,
                message1=16,
                message2_target=35,
                message2=16,
            ),
        ],
    ),
    "Processor Core": LevelData(
        room_id=41,
        entity_file="unit1_rm5",
        entities=[
            ItemSpawnEntityData(
                entity_id=23,
                item_type=ItemType.UA_EXPANSION,
            ),
        ],
    ),
    # Celestial Archives
    "Biodefense Chamber 01": LevelData(
        room_id=55,
        entity_file="Unit2_b1",
        entities=[
            ArtifactEntityData(
                entity_id=8,
                message1_target=1,
                message1=16,
            ),
        ],
    ),
    "Biodefense Chamber 05": LevelData(
        room_id=64,
        entity_file="Unit2_b2",
        entities=[
            ArtifactEntityData(
                entity_id=2,
                message1_target=4,
                message1=16,
            ),
        ],
    ),
    "Celestial Gateway": LevelData(
        room_id=45,
        entity_file="unit2_Land",
        entities=[
            ItemSpawnEntityData(
                entity_id=21,
                item_type=ItemType.UA_EXPANSION,
            ),
            ForceFieldEntityData(
                entity_id=20,
                type=ForceFieldType.BATTLEHAMMER,
            ),
        ],
    ),
    "Data Shrine 01": LevelData(
        room_id=48,
        entity_file="unit2_RM1",
        entities=[
            ItemSpawnEntityData(
                entity_id=14,
                has_base=False,
                item_type=ItemType.ENERGY_TANK,
            ),
            ArtifactEntityData(
                entity_id=2,
                has_base=False,
                message1_target=21,
                message1=18,
            ),
        ],
    ),
    "Data Shrine 02": LevelData(
        room_id=50,
        entity_file="unit2_RM2",
        entities=[
            ItemSpawnEntityData(
                entity_id=14,
                item_type=ItemType.VOLT_DRIVER,
                notify_entity_id=46,
                collected_message=9,
            ),
            ItemSpawnEntityData(
                entity_id=18,
                has_base=False,
                item_type=ItemType.MISSILE_EXPANSION,
            ),
            ItemSpawnEntityData(
                entity_id=41,
                item_type=ItemType.UA_EXPANSION,
            ),
        ],
    ),
    "Data Shrine 03": LevelData(
        room_id=52,
        entity_file="unit2_RM3",
        entities=[
            ArtifactEntityData(
                entity_id=2,
                has_base=False,
                message1_target=22,
                message1=18,
            ),
        ],
    ),
    "Docking Bay": LevelData(
        room_id=62,
        entity_file="Unit2_RM8",
        entities=[
            ItemSpawnEntityData(
                entity_id=6,
                has_base=False,
                item_type=ItemType.UA_EXPANSION,
            ),
            ArtifactEntityData(
                entity_id=1,
                has_base=False,
            ),
        ],
    ),
    "Incubation Vault 01": LevelData(
        room_id=59,
        entity_file="unit2_RM5",
        entities=[
            ArtifactEntityData(
                entity_id=10,
                has_base=False,
            ),
            ForceFieldEntityData(
                entity_id=4,
                type=ForceFieldType.SHOCK_COIL,
            ),
        ],
    ),
    "Incubation Vault 02": LevelData(
        room_id=60,
        entity_file="unit2_RM6",
        entities=[
            ItemSpawnEntityData(
                entity_id=7,
                item_type=ItemType.SHOCK_COIL,
                notify_entity_id=4,
                collected_message=18,
            ),
            ForceFieldEntityData(
                entity_id=3,
                type=ForceFieldType.SHOCK_COIL,
            ),
        ],
    ),
    "Incubation Vault 03": LevelData(
        room_id=61,
        entity_file="Unit2_RM7",
        entities=[
            ItemSpawnEntityData(
                entity_id=10,
                item_type=ItemType.MISSILE_EXPANSION,
            ),
            ForceFieldEntityData(
                entity_id=8,
                type=ForceFieldType.SHOCK_COIL,
            ),
        ],
    ),
    "New Arrival Registration": LevelData(
        room_id=57,
        entity_file="Unit2_C7",
        entities=[
            ItemSpawnEntityData(
                entity_id=21,
                item_type=ItemType.ENERGY_TANK,
            ),
            ArtifactEntityData(
                entity_id=19,
                has_base=False,
                message1_target=20,
                message1=18,
            ),
        ],
    ),
    "Synergy Core": LevelData(
        room_id=53,
        entity_file="unit2_C4",
        entities=[
            ArtifactEntityData(
                entity_id=3,
                has_base=False,
                message1_target=22,
                message1=9,
            ),
            ForceFieldEntityData(
                entity_id=15,
                type=ForceFieldType.VOLT_DRIVER,
            ),
        ],
    ),
    "Transfer Lock": LevelData(
        room_id=58,
        entity_file="Unit2_RM4",
        entities=[
            ItemSpawnEntityData(
                entity_id=64,
                item_type=ItemType.UA_EXPANSION,
            ),
        ],
    ),
    # Vesper Defense Outpost
    "Biodefense Chamber 03": LevelData(
        room_id=71,
        entity_file="Unit3_b1",
        entities=[
            ArtifactEntityData(
                entity_id=8,
                message1_target=1,
                message1=16,
            ),
        ],
    ),
    "Biodefense Chamber 08": LevelData(
        room_id=76,
        entity_file="Unit3_b2",
        entities=[
            ArtifactEntityData(
                entity_id=2,
                message1_target=4,
                message1=16,
            ),
        ],
    ),
    "Compression Chamber": LevelData(
        room_id=69,
        entity_file="unit3_rm4",
        entities=[
            ItemSpawnEntityData(
                entity_id=9,
                has_base=False,
                item_type=ItemType.UA_EXPANSION,
            ),
            ArtifactEntityData(
                entity_id=17,
                message1_target=55,
                message1=18,
            ),
            ForceFieldEntityData(
                entity_id=35,
                type=ForceFieldType.BATTLEHAMMER,
            ),
            ForceFieldEntityData(
                entity_id=36,
                type=ForceFieldType.BATTLEHAMMER,
            ),
        ],
    ),
    "Cortex CPU": LevelData(
        room_id=67,
        entity_file="Unit3_C2",
        entities=[
            ItemSpawnEntityData(
                entity_id=9,
                item_type=ItemType.BATTLEHAMMER,
                notify_entity_id=19,
                collected_message=9,
            ),
            ItemSpawnEntityData(
                entity_id=18,
                has_base=False,
                item_type=ItemType.MISSILE_EXPANSION,
            ),
            ForceFieldEntityData(
                entity_id=27,
                type=ForceFieldType.BATTLEHAMMER,
            ),
        ],
    ),
    "Fuel Stack": LevelData(
        room_id=73,
        entity_file="Unit3_RM2",
        entities=[
            ItemSpawnEntityData(
                entity_id=72,
                item_type=ItemType.MISSILE_EXPANSION,
            ),
            ArtifactEntityData(
                entity_id=12,
                has_base=False,
            ),
        ],
    ),
    "Stasis Bunker": LevelData(
        room_id=74,
        entity_file="Unit3_RM3",
        entities=[
            ItemSpawnEntityData(
                entity_id=90,
                item_type=ItemType.UA_EXPANSION,
                notify_entity_id=17,
                collected_message=18,
            ),
            ArtifactEntityData(
                entity_id=4,
                has_base=False,
                message1_target=17,
                message1=18,
            ),
            ArtifactEntityData(
                entity_id=5,
                has_base=False,
                message1_target=36,
                message1=18,
            ),
        ],
    ),
    "Weapons Complex": LevelData(
        room_id=68,
        entity_file="Unit3_RM1",
        entities=[
            ArtifactEntityData(
                entity_id=23,
                has_base=False,
            ),
            ArtifactEntityData(
                entity_id=61,
                has_base=False,
            ),
            ForceFieldEntityData(
                entity_id=9,
                type=ForceFieldType.BATTLEHAMMER,
            ),
        ],
    ),
    # Arcterra
    "Biodefense Chamber 04": LevelData(
        room_id=82,
        entity_file="Unit4_b1",
        entities=[
            ArtifactEntityData(
                entity_id=2,
                message1_target=4,
                message1=16,
                message2_target=16,
                message2=9,
            ),
        ],
    ),
    "Biodefense Chamber 07": LevelData(
        room_id=88,
        entity_file="Unit4_b2",
        entities=[
            ArtifactEntityData(
                entity_id=8,
                message1_target=1,
                message1=16,
            ),
        ],
    ),
    "Drip Moat": LevelData(
        room_id=83,
        entity_file="unit4_C1",
        entities=[
            ItemSpawnEntityData(
                entity_id=50,
                has_base=False,
                item_type=ItemType.UA_EXPANSION,
            ),
        ],
    ),
    "Fault Line": LevelData(
        room_id=86,
        entity_file="Unit4_RM5",
        entities=[
            ItemSpawnEntityData(
                entity_id=46,
                active=False,
                has_base=False,
                item_type=ItemType.IMPERIALIST,
                notify_entity_id=69,
                collected_message=18,
            ),
            ArtifactEntityData(
                entity_id=47,
                has_base=False,
            ),
        ],
    ),
    "Frost Labyrinth": LevelData(
        room_id=80,
        entity_file="unit4_C0",
        entities=[
            ItemSpawnEntityData(
                entity_id=18,
                item_type=ItemType.ENERGY_TANK,
            ),
            ArtifactEntityData(
                entity_id=6,
            ),
        ],
    ),
    "Ice Hive": LevelData(
        room_id=78,
        entity_file="Unit4_RM1",
        entities=[
            ItemSpawnEntityData(
                entity_id=1,
                item_type=ItemType.UA_EXPANSION,
            ),
            ItemSpawnEntityData(
                entity_id=6,
                item_type=ItemType.UA_EXPANSION,
            ),
            ItemSpawnEntityData(
                entity_id=7,
                has_base=False,
                item_type=ItemType.JUDICATOR,
                notify_entity_id=205,
                collected_message=9,
            ),
            ItemSpawnEntityData(
                entity_id=34,
                item_type=ItemType.MISSILE_EXPANSION,
            ),
            ArtifactEntityData(
                entity_id=26,
            ),
            ForceFieldEntityData(
                entity_id=39,
                type=ForceFieldType.JUDICATOR,
            ),
            ForceFieldEntityData(
                entity_id=4,
                type=ForceFieldType.JUDICATOR,
            ),
            ForceFieldEntityData(
                entity_id=18,
                type=ForceFieldType.JUDICATOR,
            ),
            ForceFieldEntityData(
                entity_id=59,
                type=ForceFieldType.JUDICATOR,
            ),
            ForceFieldEntityData(
                entity_id=72,
                type=ForceFieldType.JUDICATOR,
            ),
        ],
    ),
    "Sanctorus": LevelData(
        room_id=85,
        entity_file="unit4_rm4",
        entities=[
            ItemSpawnEntityData(
                entity_id=43,
                item_type=ItemType.UA_EXPANSION,
            ),
            ArtifactEntityData(
                entity_id=7,
                has_base=False,
                message1_target=38,
                message1=18,
            ),
        ],
    ),
    "Sic Transit": LevelData(
        room_id=105,
        entity_file="unit4_rm3",
        entities=[
            ItemSpawnEntityData(
                entity_id=29,
                has_base=False,
                item_type=ItemType.ENERGY_TANK,
                notify_entity_id=9,
                collected_message=16,
            ),
            ArtifactEntityData(
                entity_id=35,
                message1_target=6,
                message1=16,
                message2_target=9,
                message2=16,
            ),
        ],
    ),
    "Subterranean": LevelData(
        room_id=109,
        entity_file="Unit4_RM2",
        entities=[
            ItemSpawnEntityData(
                entity_id=57,
                item_type=ItemType.MISSILE_EXPANSION,
                notify_entity_id=56,
                collected_message=18,
            ),
            ArtifactEntityData(
                entity_id=18,
                has_base=False,
                message1_target=58,
                message1=16,
                message2_target=56,
                message2=18,
            ),
        ],
    ),
    # Oubliette
    "Gorea Peek": LevelData(
        room_id=90,
        entity_file="Gorea_Peek",
        entities=[
            ItemSpawnEntityData(
                entity_id=3,
                item_type=ItemType.ENERGY_TANK,
            ),
        ],
    ),
}


def get_data(room_name: str) -> LevelData:
    return ALL_ENTITIES_DATA[room_name]
