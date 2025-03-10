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
    entity_type: int
    item_type: str
    active: bool = True
    has_base: bool = True
    item_spawn_messages: ItemSpawnMessages | None = None
    artifact_messages: ArtifactMessages | None = None


@dataclasses.dataclass(frozen=True)
class LevelData:
    room_id: int
    entity_file: str
    entities: list[EntityData]


ALL_ENTITIES_DATA: dict[str, LevelData] = {
    # Alinos
    "Alinos Gateway": LevelData(
        room_id=27,
        entity_file="Unit1_Land",
        entities=[
            EntityData(
                entity_id=13,
                offset=2024,
                entity_type=4,
                item_type="MissileExpansion",
            ),
        ],
    ),
    "Alinos Perch": LevelData(
        room_id=39,
        entity_file="unit1_RM2",
        entities=[
            EntityData(
                entity_id=15,
                offset=4228,
                entity_type=4,
                item_type="MissileExpansion",
            ),
        ],
    ),
    "Biodefense Chamber 02": LevelData(
        room_id=35,
        entity_file="Unit1_b1",
        entities=[
            EntityData(
                entity_id=2,
                offset=1128,
                entity_type=17,
                item_type="Artifact",
                artifact_messages=ArtifactMessages(
                    message1_target=4,
                    message1=16,
                ),
            ),
        ],
    ),
    "Biodefense Chamber 06": LevelData(
        room_id=44,
        entity_file="Unit1_b2",
        entities=[
            EntityData(
                entity_id=8,
                offset=1592,
                entity_type=17,
                item_type="Artifact",
                artifact_messages=ArtifactMessages(
                    message1_target=1,
                    message1=16,
                ),
            ),
        ],
    ),
    "Council Chamber": LevelData(
        room_id=40,
        entity_file="unit1_rm3",
        entities=[
            EntityData(
                entity_id=5,
                offset=4004,
                entity_type=4,
                item_type="EnergyTank",
            ),
            EntityData(
                entity_id=19,
                offset=4076,
                entity_type=17,
                item_type="Artifact",
            ),
            EntityData(
                entity_id=21,
                offset=4148,
                entity_type=4,
                item_type="Magmaul",
                active=False,
                has_base=False,
            ),
        ],
    ),
    "Crash Site": LevelData(
        room_id=42,
        entity_file="Unit1_C3",
        entities=[
            EntityData(
                entity_id=4,
                offset=992,
                entity_type=17,
                item_type="Artifact",
                has_base=False,
            ),
        ],
    ),
    "Echo Hall": LevelData(
        room_id=28,
        entity_file="Unit1_C0",
        entities=[
            EntityData(
                entity_id=3,
                offset=1920,
                entity_type=17,
                item_type="Artifact",
            ),
            EntityData(
                entity_id=15,
                offset=3400,
                entity_type=4,
                item_type="EnergyTank",
                has_base=False,
            ),
        ],
    ),
    "Elder Passage": LevelData(
        room_id=31,
        entity_file="unit_RM6",
        entities=[
            EntityData(
                entity_id=4,
                offset=1368,
                entity_type=17,
                item_type="Artifact",
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
        room_id=29,
        entity_file="unit1_RM1",
        entities=[
            EntityData(
                entity_id=24,
                offset=5976,
                entity_type=17,
                item_type="Artifact",
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
                entity_id=80,
                offset=15872,
                entity_type=4,
                item_type="MissileExpansion",
                has_base=False,
            ),
        ],
    ),
    "Magma Drop": LevelData(
        room_id=30,
        entity_file="Unit1_C4",
        entities=[
            EntityData(
                entity_id=14,
                offset=3264,
                entity_type=4,
                item_type="UAExpansion",
            ),
        ],
    ),
    "Piston Cave": LevelData(
        room_id=38,
        entity_file="Unit1_C5",
        entities=[
            EntityData(
                entity_id=38,
                offset=17196,
                entity_type=17,
                item_type="Artifact",
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
        room_id=41,
        entity_file="unit1_rm5",
        entities=[
            EntityData(
                entity_id=23,
                offset=4888,
                entity_type=4,
                item_type="UAExpansion",
            ),
        ],
    ),
    # Celestial Archives
    "Biodefense Chamber 01": LevelData(
        room_id=55,
        entity_file="Unit2_b1",
        entities=[
            EntityData(
                entity_id=8,
                offset=1592,
                entity_type=17,
                item_type="Artifact",
                artifact_messages=ArtifactMessages(
                    message1_target=1,
                    message1=16,
                ),
            ),
        ],
    ),
    "Biodefense Chamber 05": LevelData(
        room_id=64,
        entity_file="Unit2_b2",
        entities=[
            EntityData(
                entity_id=2,
                offset=1104,
                entity_type=17,
                item_type="Artifact",
                artifact_messages=ArtifactMessages(
                    message1_target=4,
                    message1=16,
                ),
            ),
        ],
    ),
    "Celestial Gateway": LevelData(
        room_id=45,
        entity_file="unit2_Land",
        entities=[
            EntityData(
                entity_id=21,
                offset=4328,
                entity_type=4,
                item_type="UAExpansion",
            ),
        ],
    ),
    "Data Shrine 01": LevelData(
        room_id=48,
        entity_file="unit2_RM1",
        entities=[
            EntityData(
                entity_id=2,
                offset=1660,
                entity_type=17,
                item_type="Artifact",
                has_base=False,
                artifact_messages=ArtifactMessages(
                    message1_target=21,
                    message1=18,
                ),
            ),
            EntityData(
                entity_id=14,
                offset=8280,
                entity_type=4,
                item_type="EnergyTank",
                has_base=False,
            ),
        ],
    ),
    "Data Shrine 02": LevelData(
        room_id=50,
        entity_file="unit2_RM2",
        entities=[
            EntityData(
                entity_id=14,
                offset=1660,
                entity_type=4,
                item_type="VoltDriver",
                item_spawn_messages=ItemSpawnMessages(
                    notify_entity_id=46,
                    collected_message=9,
                ),
            ),
            EntityData(
                entity_id=18,
                offset=8280,
                entity_type=4,
                item_type="MissileExpansion",
                has_base=False,
            ),
            EntityData(
                entity_id=41,
                offset=8280,
                entity_type=4,
                item_type="UAExpansion",
            ),
        ],
    ),
    "Data Shrine 03": LevelData(
        room_id=52,
        entity_file="unit2_RM3",
        entities=[
            EntityData(
                entity_id=2,
                offset=1612,
                entity_type=17,
                item_type="Artifact",
                has_base=False,
                artifact_messages=ArtifactMessages(
                    message1_target=22,
                    message1=18,
                ),
            ),
        ],
    ),
    "Docking Bay": LevelData(
        room_id=62,
        entity_file="Unit2_RM8",
        entities=[
            EntityData(
                entity_id=1,
                offset=4211,
                entity_type=17,
                item_type="Artifact",
                has_base=False,
            ),
            EntityData(
                entity_id=6,
                offset=7280,
                entity_type=4,
                item_type="UAExpansion",
                has_base=False,
            ),
        ],
    ),
    "Incubation Vault 01": LevelData(
        room_id=59,
        entity_file="unit2_RM5",
        entities=[
            EntityData(
                entity_id=10,
                offset=1336,
                entity_type=17,
                item_type="Artifact",
                has_base=False,
            ),
        ],
    ),
    "Incubation Vault 02": LevelData(
        room_id=60,
        entity_file="unit2_RM6",
        entities=[
            EntityData(
                entity_id=7,
                offset=1124,
                entity_type=4,
                item_type="ShockCoil",
                item_spawn_messages=ItemSpawnMessages(
                    notify_entity_id=4,
                    collected_message=18,
                ),
            ),
        ],
    ),
    "Incubation Vault 03": LevelData(
        room_id=61,
        entity_file="Unit2_RM7",
        entities=[
            EntityData(
                entity_id=10,
                offset=944,
                entity_type=4,
                item_type="MissileExpansion",
            ),
        ],
    ),
    "New Arrival Registration": LevelData(
        room_id=57,
        entity_file="Unit2_C7",
        entities=[
            EntityData(
                entity_id=19,
                offset=7276,
                entity_type=17,
                item_type="Artifact",
                has_base=False,
                artifact_messages=ArtifactMessages(
                    message1_target=20,
                    message1=18,
                ),
            ),
            EntityData(
                entity_id=21,
                offset=11172,
                entity_type=4,
                item_type="EnergyTank",
            ),
        ],
    ),
    "Synergy Core": LevelData(
        room_id=53,
        entity_file="unit2_C4",
        entities=[
            EntityData(
                entity_id=3,
                offset=1764,
                entity_type=17,
                item_type="Artifact",
                has_base=False,
                artifact_messages=ArtifactMessages(
                    message1_target=22,
                    message1=9,
                ),
            ),
        ],
    ),
    "Transfer Lock": LevelData(
        room_id=58,
        entity_file="Unit2_RM4",
        entities=[
            EntityData(
                entity_id=64,
                offset=17316,
                entity_type=4,
                item_type="UAExpansion",
            ),
        ],
    ),
    # Vesper Defense Outpost
    "Biodefense Chamber 03": LevelData(
        room_id=71,
        entity_file="Unit3_b1",
        entities=[
            EntityData(
                entity_id=8,
                offset=1592,
                entity_type=17,
                item_type="Artifact",
                artifact_messages=ArtifactMessages(
                    message1_target=1,
                    message1=16,
                ),
            ),
        ],
    ),
    "Biodefense Chamber 08": LevelData(
        room_id=76,
        entity_file="Unit3_b2",
        entities=[
            EntityData(
                entity_id=2,
                offset=1152,
                entity_type=17,
                item_type="Artifact",
                artifact_messages=ArtifactMessages(
                    message1_target=4,
                    message1=16,
                ),
            ),
        ],
    ),
    "Compression Chamber": LevelData(
        room_id=69,
        entity_file="unit3_rm4",
        entities=[
            EntityData(
                entity_id=9,
                offset=6368,
                entity_type=4,
                item_type="UAExpansion",
                has_base=False,
            ),
            EntityData(
                entity_id=17,
                offset=3496,
                entity_type=17,
                item_type="Artifact",
                artifact_messages=ArtifactMessages(
                    message1_target=55,
                    message1=18,
                ),
            ),
        ],
    ),
    "Cortex CPU": LevelData(
        room_id=67,
        entity_file="Unit3_C2",
        entities=[
            EntityData(
                entity_id=9,
                offset=2080,
                entity_type=4,
                item_type="Battlehammer",
                item_spawn_messages=ItemSpawnMessages(
                    notify_entity_id=19,
                    collected_message=9,
                ),
            ),
            EntityData(
                entity_id=18,
                offset=5828,
                entity_type=4,
                item_type="MissileExpansion",
                has_base=False,
            ),
        ],
    ),
    "Fuel Stack": LevelData(
        room_id=73,
        entity_file="Unit3_RM2",
        entities=[
            EntityData(
                entity_id=12,
                offset=8128,
                entity_type=17,
                item_type="Artifact",
                has_base=False,
            ),
            EntityData(
                entity_id=72,
                offset=17768,
                entity_type=4,
                item_type="MissileExpansion",
            ),
        ],
    ),
    "Stasis Bunker": LevelData(
        room_id=74,
        entity_file="Unit3_RM3",
        entities=[
            EntityData(
                entity_id=4,
                offset=7352,
                entity_type=17,
                item_type="Artifact",
                has_base=False,
                artifact_messages=ArtifactMessages(
                    message1_target=17,
                    message1=18,
                ),
            ),
            EntityData(
                entity_id=5,
                offset=2432,
                entity_type=17,
                item_type="Artifact",
                has_base=False,
                artifact_messages=ArtifactMessages(
                    message1_target=36,
                    message1=18,
                ),
            ),
            EntityData(
                entity_id=90,
                offset=19804,
                entity_type=4,
                item_type="UAExpansion",
                item_spawn_messages=ItemSpawnMessages(
                    notify_entity_id=17,
                    collected_message=18,
                ),
            ),
        ],
    ),
    "Weapons Complex": LevelData(
        room_id=68,
        entity_file="Unit3_RM1",
        entities=[
            EntityData(
                entity_id=23,
                offset=5572,
                entity_type=17,
                item_type="Artifact",
                has_base=False,
            ),
            EntityData(
                entity_id=61,
                offset=2228,
                entity_type=17,
                item_type="Artifact",
                has_base=False,
            ),
        ],
    ),
    # Arcterra
    "Biodefense Chamber 04": LevelData(
        room_id=82,
        entity_file="Unit4_b1",
        entities=[
            EntityData(
                entity_id=2,
                offset=1128,
                entity_type=17,
                item_type="Artifact",
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
        room_id=88,
        entity_file="Unit4_b2",
        entities=[
            EntityData(
                entity_id=8,
                offset=1592,
                entity_type=17,
                item_type="Artifact",
                artifact_messages=ArtifactMessages(
                    message1_target=1,
                    message1=16,
                ),
            ),
        ],
    ),
    "Drip Moat": LevelData(
        room_id=83,
        entity_file="unit4_C1",
        entities=[
            EntityData(
                entity_id=50,
                offset=23796,
                entity_type=4,
                item_type="UAExpansion",
                has_base=False,
            ),
        ],
    ),
    "Fault Line": LevelData(
        room_id=86,
        entity_file="Unit4_RM5",
        entities=[
            EntityData(
                entity_id=46,
                offset=4288,
                entity_type=4,
                item_type="Imperialist",
                active=False,
                has_base=False,
                item_spawn_messages=ItemSpawnMessages(
                    notify_entity_id=69,
                    collected_message=18,
                ),
            ),
            EntityData(
                entity_id=47,
                offset=4360,
                entity_type=17,
                item_type="Artifact",
                has_base=False,
            ),
        ],
    ),
    "Frost Labyrinth": LevelData(
        room_id=80,
        entity_file="unit4_C0",
        entities=[
            EntityData(
                entity_id=6,
                offset=2552,
                entity_type=17,
                item_type="Artifact",
            ),
            EntityData(
                entity_id=18,
                offset=8720,
                entity_type=4,
                item_type="EnergyTank",
            ),
        ],
    ),
    "Ice Hive": LevelData(
        room_id=78,
        entity_file="Unit4_RM1",
        entities=[
            EntityData(
                entity_id=1,
                offset=11116,
                entity_type=4,
                item_type="UAExpansion",
            ),
            EntityData(
                entity_id=6,
                offset=52688,
                entity_type=4,
                item_type="UAExpansion",
            ),
            EntityData(
                entity_id=7,
                offset=10232,
                entity_type=4,
                item_type="Judicator",
                has_base=False,
                item_spawn_messages=ItemSpawnMessages(
                    notify_entity_id=205,
                    collected_message=9,
                ),
            ),
            EntityData(
                entity_id=26,
                offset=5596,
                entity_type=17,
                item_type="Artifact",
            ),
            EntityData(
                entity_id=34,
                offset=24512,
                entity_type=4,
                item_type="MissileExpansion",
            ),
        ],
    ),
    "Sanctorus": LevelData(
        room_id=85,
        entity_file="unit4_rm4",
        entities=[
            EntityData(
                entity_id=7,
                offset=2256,
                entity_type=17,
                item_type="Artifact",
                has_base=False,
                artifact_messages=ArtifactMessages(
                    message1_target=38,
                    message1=18,
                ),
            ),
            EntityData(
                entity_id=43,
                offset=12176,
                entity_type=4,
                item_type="UAExpansion",
            ),
        ],
    ),
    "Sic Transit": LevelData(
        room_id=105,
        entity_file="unit4_rm3",
        entities=[
            EntityData(
                entity_id=29,
                offset=5068,
                entity_type=4,
                item_type="EnergyTank",
                has_base=False,
                item_spawn_messages=ItemSpawnMessages(
                    notify_entity_id=9,
                    collected_message=16,
                ),
            ),
            EntityData(
                entity_id=35,
                offset=6844,
                entity_type=17,
                item_type="Artifact",
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
        room_id=109,
        entity_file="Unit4_RM2",
        entities=[
            EntityData(
                entity_id=18,
                offset=4360,
                entity_type=17,
                item_type="Artifact",
                has_base=False,
                artifact_messages=ArtifactMessages(
                    message1_target=58,
                    message1=16,
                    message2_target=56,
                    message2=18,
                ),
            ),
            EntityData(
                entity_id=57,
                offset=7804,
                entity_type=4,
                item_type="MissileExpansion",
                item_spawn_messages=ItemSpawnMessages(
                    notify_entity_id=56,
                    collected_message=18,
                ),
            ),
        ],
    ),
    # Oubliette
    "Gorea Peek": LevelData(
        room_id=90,
        entity_file="Gorea_Peek",
        entities=[
            EntityData(
                entity_id=1,
                offset=268,
                entity_type=4,
                item_type="EnergyTank",
            ),
        ],
    ),
}


def get_data(room_name: str) -> LevelData:
    return ALL_ENTITIES_DATA[room_name]
