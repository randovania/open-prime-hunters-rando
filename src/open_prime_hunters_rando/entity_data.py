import dataclasses


@dataclasses.dataclass(frozen=True)
class ItemSpawnMessages:
    notify_entity_id: int = 0
    collected_message: int = 0


@dataclasses.dataclass(frozen=True)
class ArtifactMessages:
    message1_target: int = 0
    message1: int = 0
    message2_target: int = 0
    message2: int = 0
    message3_target: int = 0
    message3: int = 0


@dataclasses.dataclass(frozen=True)
class EntityData:
    entity_id: int
    offset: int
    item_type: str = ""
    active: bool = True
    has_base: bool = True
    item_spawn_messages: ItemSpawnMessages | None = None
    artifact_messages: ArtifactMessages | None = None


@dataclasses.dataclass(frozen=True)
class LevelData:
    entity_file: str
    entities: list[EntityData]


ITEM_ENTITIES_DATA: dict[str, LevelData] = {
    # Alinos
    "Alinos Gateway": LevelData(
        entity_file="Unit1_Land",
        entities=[
            EntityData(
                item_type="MissileExpansion",
                entity_id=13,
                offset=2024,
            ),
        ],
    ),
    "Alinos Perch": LevelData(
        entity_file="unit1_RM2",
        entities=[
            EntityData(
                item_type="MissileExpansion",
                entity_id=15,
                offset=4228,
            ),
        ],
    ),
    "Biodefense Chamber 02": LevelData(
        entity_file="Unit1_b1",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=2,
                offset=1128,
                artifact_messages=ArtifactMessages(
                    message1_target=4,
                    message1=16,
                ),
            ),
        ],
    ),
    "Biodefense Chamber 06": LevelData(
        entity_file="Unit1_b2",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=8,
                offset=1592,
                artifact_messages=ArtifactMessages(
                    message1_target=1,
                    message1=16,
                ),
            ),
        ],
    ),
    "Council Chamber": LevelData(
        entity_file="unit1_rm3",
        entities=[
            EntityData(
                item_type="EnergyTank",
                entity_id=5,
                offset=4004,
            ),
            EntityData(
                item_type="Artifact",
                entity_id=19,
                offset=4076,
            ),
            EntityData(
                item_type="Magmaul",
                entity_id=21,
                offset=4148,
                active=False,
                has_base=False,
            ),
        ],
    ),
    "Crash Site": LevelData(
        entity_file="Unit1_C3",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=4,
                offset=992,
                has_base=False,
            ),
        ],
    ),
    "Echo Hall": LevelData(
        entity_file="Unit1_C0",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=3,
                offset=1920,
            ),
            EntityData(
                item_type="EnergyTank",
                entity_id=15,
                offset=3400,
                has_base=False,
            ),
        ],
    ),
    "Elder Passage": LevelData(
        entity_file="unit_RM6",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=4,
                offset=1368,
                has_base=False,
                artifact_messages=ArtifactMessages(
                    message1_target=40,
                    message1=9,
                    message2_target=1,
                    message2=9,
                ),
            ),
        ],
    ),
    "High Ground": LevelData(
        entity_file="unit1_RM1",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=24,
                offset=5976,
                has_base=False,
                artifact_messages=ArtifactMessages(
                    message1_target=17,
                    message1=16,
                    message2_target=56,
                    message2=33,
                    message3_target=94,
                    message3=9,
                ),
            ),
            EntityData(
                item_type="MissileExpansion",
                entity_id=80,
                offset=15872,
                has_base=False,
            ),
        ],
    ),
    "Magma Drop": LevelData(
        entity_file="Unit1_C4",
        entities=[
            EntityData(
                item_type="UAExpansion",
                entity_id=14,
                offset=3264,
            ),
        ],
    ),
    "Piston Cave": LevelData(
        entity_file="Unit1_C5",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=38,
                offset=17196,
                has_base=False,
                artifact_messages=ArtifactMessages(
                    message1_target=36,
                    message1=16,
                    message2_target=35,
                    message2=16,
                ),
            ),
        ],
    ),
    "Processor Core": LevelData(
        entity_file="unit1_rm5",
        entities=[
            EntityData(
                item_type="UAExpansion",
                entity_id=23,
                offset=4888,
            ),
        ],
    ),
    # Celestial Archives
    "Biodefense Chamber 01": LevelData(
        entity_file="Unit2_b1",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=8,
                offset=1592,
                artifact_messages=ArtifactMessages(
                    message1_target=1,
                    message1=16,
                ),
            ),
        ],
    ),
    "Biodefense Chamber 05": LevelData(
        entity_file="Unit2_b2",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=2,
                offset=1104,
                artifact_messages=ArtifactMessages(
                    message1_target=4,
                    message1=16,
                ),
            ),
        ],
    ),
    "Celestial Gateway": LevelData(
        entity_file="unit2_Land",
        entities=[
            EntityData(
                item_type="UAExpansion",
                entity_id=21,
                offset=4328,
            ),
        ],
    ),
    "Data Shrine 01": LevelData(
        entity_file="unit2_RM1",
        entities=[
            EntityData(
                entity_id=2,
                offset=1660,
                has_base=False,
                artifact_messages=ArtifactMessages(
                    message1_target=21,
                    message1=18,
                ),
            ),
            EntityData(
                item_type="EnergyTank",
                entity_id=14,
                offset=8280,
                has_base=False,
            ),
        ],
    ),
    "Data Shrine 02": LevelData(
        entity_file="unit2_RM2",
        entities=[
            EntityData(
                item_type="VoltDriver",
                entity_id=14,
                offset=1660,
                item_spawn_messages=ItemSpawnMessages(
                    notify_entity_id=46,
                    collected_message=9,
                ),
            ),
            EntityData(
                item_type="MissileExpansion",
                entity_id=18,
                offset=8280,
                has_base=False,
            ),
            EntityData(
                item_type="UAExpansion",
                entity_id=41,
                offset=8280,
            ),
        ],
    ),
    "Data Shrine 03": LevelData(
        entity_file="unit2_RM3",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=2,
                offset=1612,
                has_base=False,
                artifact_messages=ArtifactMessages(
                    message1_target=22,
                    message1=18,
                ),
            ),
        ],
    ),
    "Docking Bay": LevelData(
        entity_file="Unit2_RM8",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=1,
                offset=4211,
                has_base=False,
            ),
            EntityData(
                item_type="UAExpansion",
                entity_id=6,
                offset=7280,
                has_base=False,
            ),
        ],
    ),
    "Incubation Vault 01": LevelData(
        entity_file="unit2_RM5",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=10,
                offset=1336,
                has_base=False,
            ),
        ],
    ),
    "Incubation Vault 02": LevelData(
        entity_file="unit2_RM6",
        entities=[
            EntityData(
                item_type="ShockCoil",
                entity_id=7,
                offset=1124,
                item_spawn_messages=ItemSpawnMessages(
                    notify_entity_id=4,
                    collected_message=18,
                ),
            ),
        ],
    ),
    "Incubation Vault 03": LevelData(
        entity_file="Unit2_RM7",
        entities=[
            EntityData(
                item_type="MissileExpansion",
                entity_id=10,
                offset=944,
            ),
        ],
    ),
    "New Arrival Registration": LevelData(
        entity_file="Unit2_C7",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=19,
                offset=7276,
                has_base=False,
                artifact_messages=ArtifactMessages(
                    message1_target=20,
                    message1=18,
                ),
            ),
            EntityData(
                item_type="EnergyTank",
                entity_id=21,
                offset=11172,
            ),
        ],
    ),
    "Synergy Core": LevelData(
        entity_file="unit2_C4",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=3,
                offset=1764,
                has_base=False,
                artifact_messages=ArtifactMessages(
                    message1_target=22,
                    message1=9,
                ),
            ),
        ],
    ),
    "Transfer Lock": LevelData(
        entity_file="Unit2_RM4",
        entities=[
            EntityData(
                item_type="UAExpansion",
                entity_id=64,
                offset=17316,
            ),
        ],
    ),
    # Vesper Defense Outpost
    "Biodefense Chamber 03": LevelData(
        entity_file="Unit3_b1",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=8,
                offset=1592,
                artifact_messages=ArtifactMessages(
                    message1_target=1,
                    message1=16,
                ),
            ),
        ],
    ),
    "Biodefense Chamber 08": LevelData(
        entity_file="Unit3_b2",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=2,
                offset=1152,
                artifact_messages=ArtifactMessages(
                    message1_target=4,
                    message1=16,
                ),
            ),
        ],
    ),
    "Compression Chamber": LevelData(
        entity_file="unit3_rm4",
        entities=[
            EntityData(
                item_type="UAExpansion",
                entity_id=9,
                offset=6368,
                has_base=False,
            ),
            EntityData(
                item_type="Artifact",
                entity_id=17,
                offset=3496,
                artifact_messages=ArtifactMessages(
                    message1_target=55,
                    message1=18,
                ),
            ),
        ],
    ),
    "Cortex CPU": LevelData(
        entity_file="Unit3_C2",
        entities=[
            EntityData(
                item_type="Battlehammer",
                entity_id=9,
                offset=2080,
                item_spawn_messages=ItemSpawnMessages(
                    notify_entity_id=19,
                    collected_message=9,
                ),
            ),
            EntityData(
                item_type="MissileExpansion",
                entity_id=18,
                offset=5828,
                has_base=False,
            ),
        ],
    ),
    "Fuel Stack": LevelData(
        entity_file="Unit3_RM2",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=12,
                offset=8128,
                has_base=False,
            ),
            EntityData(
                item_type="MissileExpansion",
                entity_id=72,
                offset=17768,
            ),
        ],
    ),
    "Stasis Bunker": LevelData(
        entity_file="Unit3_RM3",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=4,
                offset=7352,
                has_base=False,
                artifact_messages=ArtifactMessages(
                    message1_target=17,
                    message1=18,
                ),
            ),
            EntityData(
                item_type="Artifact",
                entity_id=5,
                offset=2432,
                has_base=False,
                artifact_messages=ArtifactMessages(
                    message1_target=36,
                    message1=18,
                ),
            ),
            EntityData(
                item_type="UAExpansion",
                entity_id=90,
                offset=19804,
                item_spawn_messages=ItemSpawnMessages(
                    notify_entity_id=17,
                    collected_message=18,
                ),
            ),
        ],
    ),
    "Weapons Complex": LevelData(
        entity_file="Unit3_RM1",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=23,
                offset=5572,
                has_base=False,
            ),
            EntityData(
                item_type="Artifact",
                entity_id=61,
                offset=2228,
                has_base=False,
            ),
        ],
    ),
    # Arcterra
    "Biodefense Chamber 04": LevelData(
        entity_file="Unit4_b1",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=2,
                offset=1128,
                artifact_messages=ArtifactMessages(
                    message1_target=4,
                    message1=16,
                    message2_target=16,
                    message2=9,
                ),
            ),
        ],
    ),
    "Biodefense Chamber 07": LevelData(
        entity_file="Unit4_b2",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=8,
                offset=1592,
                artifact_messages=ArtifactMessages(
                    message1_target=1,
                    message1=16,
                ),
            ),
        ],
    ),
    "Drip Moat": LevelData(
        entity_file="unit4_C1",
        entities=[
            EntityData(
                item_type="UAExpansion",
                entity_id=50,
                offset=23796,
                has_base=False,
            ),
        ],
    ),
    "Fault Line": LevelData(
        entity_file="Unit4_RM5",
        entities=[
            EntityData(
                item_type="Imperialist",
                entity_id=46,
                offset=4288,
                active=False,
                has_base=False,
                item_spawn_messages=ItemSpawnMessages(
                    notify_entity_id=69,
                    collected_message=18,
                ),
            ),
            EntityData(
                item_type="Artifact",
                entity_id=47,
                offset=4360,
                has_base=False,
            ),
        ],
    ),
    "Frost Labyrinth": LevelData(
        entity_file="unit4_C0",
        entities=[
            EntityData(entity_id=6, offset=2552),
            EntityData(
                item_type="EnergyTank",
                entity_id=18,
                offset=8720,
            ),
        ],
    ),
    "Ice Hive": LevelData(
        entity_file="Unit4_RM1",
        entities=[
            EntityData(
                item_type="UAExpansion",
                entity_id=1,
                offset=11116,
            ),
            EntityData(
                item_type="UAExpansion",
                entity_id=6,
                offset=52688,
            ),
            EntityData(
                item_type="Judicator",
                entity_id=7,
                offset=10232,
                has_base=False,
                item_spawn_messages=ItemSpawnMessages(
                    notify_entity_id=205,
                    collected_message=9,
                ),
            ),
            EntityData(
                item_type="Artifact",
                entity_id=26,
                offset=5596,
            ),
            EntityData(
                item_type="MissileExpansion",
                entity_id=34,
                offset=24512,
            ),
        ],
    ),
    "Sanctorus": LevelData(
        entity_file="unit4_rm4",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=7,
                offset=2256,
                has_base=False,
                artifact_messages=ArtifactMessages(
                    message1_target=38,
                    message1=18,
                ),
            ),
            EntityData(
                item_type="UAExpansion",
                entity_id=43,
                offset=12176,
            ),
        ],
    ),
    "Sic Transit": LevelData(
        entity_file="unit4_rm3",
        entities=[
            EntityData(
                item_type="EnergyTank",
                entity_id=29,
                offset=5068,
                has_base=False,
                item_spawn_messages=ItemSpawnMessages(
                    notify_entity_id=9,
                    collected_message=16,
                ),
            ),
            EntityData(
                item_type="Artifact",
                entity_id=35,
                offset=6844,
                artifact_messages=ArtifactMessages(
                    message1_target=6,
                    message1=16,
                    message2_target=9,
                    message2=16,
                ),
            ),
        ],
    ),
    "Subterranean": LevelData(
        entity_file="Unit4_RM2",
        entities=[
            EntityData(
                item_type="Artifact",
                entity_id=18,
                offset=4360,
                has_base=False,
                artifact_messages=ArtifactMessages(
                    message1_target=58,
                    message1=16,
                    message2_target=56,
                    message2=18,
                ),
            ),
            EntityData(
                item_type="MissileExpansion",
                entity_id=57,
                offset=7804,
                item_spawn_messages=ItemSpawnMessages(
                    notify_entity_id=56,
                    collected_message=18,
                ),
            ),
        ],
    ),
    # Oubliette
    "Gorea Peek": LevelData(
        entity_file="Gorea_Peek",
        entities=[
            EntityData(
                item_type="EnergyTank",
                entity_id=1,
                offset=268,
            ),
        ],
    ),
}


def get_data(room_name: str) -> LevelData:
    return ITEM_ENTITIES_DATA[room_name]
