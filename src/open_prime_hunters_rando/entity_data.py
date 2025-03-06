import dataclasses


@dataclasses.dataclass(frozen=True)
class EntityData:
    item_type: str
    entity_id: int
    offset: int
    active: bool = True
    has_base: bool = True


@dataclasses.dataclass(frozen=True)
class LevelData:
    entity_file: str
    entities: list[EntityData]


ITEM_ENTITIES_DATA: dict[str, LevelData] = {
    # Alinos
    "Alinos Gateway": LevelData(
        entity_file="Unit1_Land",
        entities=[
            EntityData(item_type="MissileExpansion", entity_id=13, offset=2024),
        ],
    ),
    "Alinos Perch": LevelData(
        entity_file="unit1_RM2",
        entities=[
            EntityData(item_type="MissileExpansion", entity_id=15, offset=4228),
        ],
    ),
    "Biodefense Chamber 02": LevelData(
        entity_file="Unit1_b1",
        entities=[
            EntityData(item_type="Artifact", entity_id=2, offset=1128),
        ],
    ),
    "Biodefense Chamber 06": LevelData(
        entity_file="Unit1_b2",
        entities=[
            EntityData(item_type="Artifact", entity_id=8, offset=1592),
        ],
    ),
    "Council Chamber": LevelData(
        entity_file="unit1_rm3",
        entities=[
            EntityData(item_type="EnergyTank", entity_id=5, offset=4004),
            EntityData(item_type="Artifact", entity_id=19, offset=4076),
            EntityData(item_type="Magmaul", entity_id=21, offset=4148, active=False, has_base=False),
        ],
    ),
    "Crash Site": LevelData(
        entity_file="Unit1_C3",
        entities=[
            EntityData(item_type="Artifact", entity_id=4, offset=992, has_base=False),
        ],
    ),
    "Echo Hall": LevelData(
        entity_file="Unit1_C0",
        entities=[
            EntityData(item_type="Artifact", entity_id=3, offset=1920),
            EntityData(item_type="EnergyTank", entity_id=15, offset=3400, has_base=False),
        ],
    ),
    "Elder Passage": LevelData(
        entity_file="unit_RM6",
        entities=[
            EntityData(item_type="Artifact", entity_id=4, offset=1368, has_base=False),
        ],
    ),
    "High Ground": LevelData(
        entity_file="unit1_RM1",
        entities=[
            EntityData(item_type="Artifact", entity_id=24, offset=5976, has_base=False),
            EntityData(item_type="MissileExpansion", entity_id=80, offset=15872, has_base=False),
        ],
    ),
    "Magma Drop": LevelData(
        entity_file="Unit1_C4",
        entities=[
            EntityData(item_type="UAExpansion", entity_id=14, offset=3264),
        ],
    ),
    "Piston Cave": LevelData(
        entity_file="Unit1_C5",
        entities=[
            EntityData(item_type="Artifact", entity_id=38, offset=17196, has_base=False),
        ],
    ),
    "Processor Core": LevelData(
        entity_file="unit1_rm5",
        entities=[
            EntityData(item_type="UAExpansion", entity_id=23, offset=4888),
        ],
    ),
    # Celestial Archives
    "Biodefense Chamber 01": LevelData(
        entity_file="Unit2_b1",
        entities=[
            EntityData(item_type="Artifact", entity_id=8, offset=1592),
        ],
    ),
    "Biodefense Chamber 05": LevelData(
        entity_file="Unit2_b2",
        entities=[
            EntityData(item_type="Artifact", entity_id=2, offset=1104),
        ],
    ),
    "Celestial Gateway": LevelData(
        entity_file="unit2_Land",
        entities=[
            EntityData(item_type="UAExpansion", entity_id=21, offset=4328),
        ],
    ),
    "Data Shrine 01": LevelData(
        entity_file="unit2_RM1",
        entities=[
            EntityData(item_type="Artifact", entity_id=2, offset=1660, has_base=False),
            EntityData(item_type="EnergyTank", entity_id=14, offset=8280, has_base=False),
        ],
    ),
    "Data Shrine 02": LevelData(
        entity_file="unit2_RM2",
        entities=[
            EntityData(item_type="VoltDriver", entity_id=14, offset=1660),
            EntityData(item_type="MissileExpansion", entity_id=18, offset=8280, has_base=False),
            EntityData(item_type="UAExpansion", entity_id=41, offset=8280),
        ],
    ),
    "Data Shrine 03": LevelData(
        entity_file="unit2_RM3",
        entities=[
            EntityData(item_type="Artifact", entity_id=2, offset=1612, has_base=False),
        ],
    ),
    "Docking Bay": LevelData(
        entity_file="Unit2_RM8",
        entities=[
            EntityData(item_type="Artifact", entity_id=1, offset=4211, has_base=False),
            EntityData(item_type="UAExpansion", entity_id=6, offset=7280, has_base=False),
        ],
    ),
    "Incubation Vault 01": LevelData(
        entity_file="unit2_RM5",
        entities=[
            EntityData(item_type="Artifact", entity_id=10, offset=1336, has_base=False),
        ],
    ),
    "Incubation Vault 02": LevelData(
        entity_file="unit2_RM6",
        entities=[
            EntityData(item_type="ShockCoil", entity_id=7, offset=1124),
        ],
    ),
    "Incubation Vault 03": LevelData(
        entity_file="Unit2_RM7",
        entities=[
            EntityData(item_type="MissileExpansion", entity_id=10, offset=944),
        ],
    ),
    "New Arrival Registration": LevelData(
        entity_file="Unit2_C7",
        entities=[
            EntityData(item_type="Artifact", entity_id=19, offset=7276, has_base=False),
            EntityData(item_type="EnergyTank", entity_id=21, offset=11172),
        ],
    ),
    "Synergy Core": LevelData(
        entity_file="unit2_C4",
        entities=[
            EntityData(item_type="Artifact", entity_id=3, offset=1764, has_base=False),
        ],
    ),
    "Transfer Lock": LevelData(
        entity_file="Unit2_RM4",
        entities=[
            EntityData(item_type="UAExpansion", entity_id=64, offset=17316),
        ],
    ),
    # Vesper Defense Outpost
    "Biodefense Chamber 03": LevelData(
        entity_file="Unit3_b1",
        entities=[
            EntityData(item_type="Artifact", entity_id=8, offset=1592),
        ],
    ),
    "Biodefense Chamber 08": LevelData(
        entity_file="Unit3_b2",
        entities=[
            EntityData(item_type="Artifact", entity_id=2, offset=1152),
        ],
    ),
    "Compression Chamber": LevelData(
        entity_file="unit3_rm4",
        entities=[
            EntityData(item_type="UAExpansion", entity_id=9, offset=6368, has_base=False),
            EntityData(item_type="Artifact", entity_id=17, offset=3496),
        ],
    ),
    "Cortex CPU": LevelData(
        entity_file="Unit3_C2",
        entities=[
            EntityData(item_type="Battlehammer", entity_id=9, offset=2080),
            EntityData(item_type="MissileExpansion", entity_id=18, offset=5828, has_base=False),
        ],
    ),
    "Fuel Stack": LevelData(
        entity_file="Unit3_RM2",
        entities=[
            EntityData(item_type="Artifact", entity_id=12, offset=8128, has_base=False),
            EntityData(item_type="MissileExpansion", entity_id=72, offset=17768),
        ],
    ),
    "Stasis Bunker": LevelData(
        entity_file="Unit3_RM3",
        entities=[
            EntityData(item_type="Artifact", entity_id=4, offset=7352, has_base=False),
            EntityData(item_type="Artifact", entity_id=5, offset=2432, has_base=False),
        ],
    ),
    "Weapons Complex": LevelData(
        entity_file="Unit3_RM1",
        entities=[
            EntityData(item_type="Artifact", entity_id=23, offset=5572, has_base=False),
            EntityData(item_type="Artifact", entity_id=61, offset=2228, has_base=False),
            EntityData(item_type="UAExpansion", entity_id=90, offset=19804),
        ],
    ),
    # Arcterra
    "Biodefense Chamber 04": LevelData(
        entity_file="Unit4_b1",
        entities=[
            EntityData(item_type="Artifact", entity_id=2, offset=1128),
        ],
    ),
    "Biodefense Chamber 07": LevelData(
        entity_file="Unit4_b2",
        entities=[
            EntityData(item_type="Artifact", entity_id=8, offset=1592),
        ],
    ),
    "Drip Moat": LevelData(
        entity_file="unit4_C1",
        entities=[
            EntityData(item_type="UAExpansion", entity_id=50, offset=23796, has_base=False),
        ],
    ),
    "Fault Line": LevelData(
        entity_file="Unit4_RM5",
        entities=[
            EntityData(item_type="Imperialist", entity_id=46, offset=4288, active=False, has_base=False),
            EntityData(item_type="Artifact", entity_id=47, offset=4360, has_base=False),
        ],
    ),
    "Frost Labyrinth": LevelData(
        entity_file="unit4_C0",
        entities=[
            EntityData(item_type="Artifact", entity_id=6, offset=2552),
            EntityData(item_type="EnergyTank", entity_id=18, offset=8720),
        ],
    ),
    "Ice Hive": LevelData(
        entity_file="Unit4_RM1",
        entities=[
            EntityData(item_type="UAExpansion", entity_id=1, offset=11116),
            EntityData(item_type="UAExpansion", entity_id=6, offset=52688),
            EntityData(item_type="Judicator", entity_id=7, offset=10232, has_base=False),
            EntityData(item_type="Artifact", entity_id=26, offset=5596),
            EntityData(item_type="MissileExpansion", entity_id=34, offset=24512),
        ],
    ),
    "Sanctorus": LevelData(
        entity_file="unit4_rm4",
        entities=[
            EntityData(item_type="Artifact", entity_id=7, offset=2256, has_base=False),
            EntityData(item_type="UAExpansion", entity_id=43, offset=12176),
        ],
    ),
    "Sic Transit": LevelData(
        entity_file="unit4_rm3",
        entities=[
            EntityData(item_type="EnergyTank", entity_id=29, offset=5068, has_base=False),
            EntityData(item_type="Artifact", entity_id=35, offset=6844),
        ],
    ),
    "Subterranean": LevelData(
        entity_file="Unit4_RM2",
        entities=[
            EntityData(item_type="Artifact", entity_id=18, offset=4360, has_base=False),
            EntityData(item_type="MissileExpansion", entity_id=57, offset=7804),
        ],
    ),
    # Oubliette
    "Gorea Peek": LevelData(
        entity_file="Gorea_Peek",
        entities=[
            EntityData(item_type="EnergyTank", entity_id=1, offset=268),
        ],
    ),
}


def get_data(room_name: str) -> LevelData:
    return ITEM_ENTITIES_DATA[room_name]
