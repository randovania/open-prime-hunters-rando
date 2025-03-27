import dataclasses


@dataclasses.dataclass(frozen=True)
class LevelData:
    room_id: int
    area_name: str
    entity_file: str | None = None


CONNECTORS: dict[str, LevelData] = {
    "Alinos Connector X": LevelData(
        room_id=0,
        area_name="Alinos",
    ),
    "Alinos Connector Z": LevelData(
        room_id=2,
        area_name="Alinos",
    ),
    "Alinos Morph Connector X": LevelData(
        room_id=4,
        area_name="Alinos",
    ),
    "Alinos Morph Connector Z": LevelData(
        room_id=6,
        area_name="Alinos",
    ),
    "Celestial Archives Connector X": LevelData(
        room_id=8,
        area_name="Celestial Archives",
    ),
    "Celestial Archives Connector Z": LevelData(
        room_id=10,
        area_name="Celestial Archives",
    ),
    "VDO Connector X": LevelData(
        room_id=12,
        area_name="Vesper Defense Outpost",
    ),
    "VDO Connector Z": LevelData(
        room_id=14,
        area_name="Vesper Defense Outpost",
    ),
    "Arcterra Connector X": LevelData(
        room_id=16,
        area_name="Arcterra",
    ),
    "Arcterra Connector Z": LevelData(
        room_id=18,
        area_name="Arcterra",
    ),
    "Alinos Connector CX": LevelData(
        room_id=20,
        area_name="Alinos",
    ),
    "Alinos Connector CZ": LevelData(
        room_id=21,
        area_name="Alinos",
    ),
    "Alinos Small Connector X": LevelData(
        room_id=22,
        area_name="Alinos",
    ),
    "Oubliette Connector Z": LevelData(
        room_id=24,
        area_name="Oubliette",
    ),
    "VDO Morph Connector Z": LevelData(
        room_id=25,
        area_name="Vesper Defense Outpost",
    ),
}

ALINOS: dict[str, LevelData] = {
    "Alinos Gateway": LevelData(
        room_id=27,
        area_name="Alinos",
        entity_file="Unit1_Land",
    ),
    "Echo Hall": LevelData(
        room_id=28,
        area_name="Alinos",
        entity_file="Unit1_C0",
    ),
    "High Ground": LevelData(
        room_id=29,
        area_name="Alinos",
        entity_file="unit1_RM1",
    ),
    "Magma Drop": LevelData(
        room_id=30,
        area_name="Alinos",
        entity_file="Unit1_C4",
    ),
    "Elder Passage": LevelData(
        room_id=31,
        area_name="Alinos",
        entity_file="unit1_RM6",
    ),
    "Alimbic Cannon Control Room": LevelData(
        room_id=32,
        area_name="Alinos",
        entity_file="crystalroom",
    ),
    "Combat Hall": LevelData(
        room_id=33,
        area_name="Alinos",
        entity_file="unit1_rm4",
    ),
    "Stronghold Void B": LevelData(
        room_id=34,
        area_name="Alinos",
        entity_file="Unit1_TP1",
    ),
    "Biodefense Chamber B": LevelData(
        room_id=35,
        area_name="Alinos",
        entity_file="Unit1_b1",
    ),
    "Alimbic Gardens": LevelData(
        room_id=36,
        area_name="Alinos",
        entity_file="Unit1_C1",
    ),
    "Thermal Vast": LevelData(
        room_id=37,
        area_name="Alinos",
        entity_file="Unit1_C2",
    ),
    "Piston Cave": LevelData(
        room_id=38,
        area_name="Alinos",
        entity_file="Unit1_C5",
    ),
    "Alinos Perch": LevelData(
        room_id=39,
        area_name="Alinos",
        entity_file="unit1_RM2",
    ),
    "Council Chamber": LevelData(
        room_id=40,
        area_name="Alinos",
        entity_file="unit1_rm3",
    ),
    "Processor Core": LevelData(
        room_id=41,
        area_name="Alinos",
        entity_file="unit1_rm5",
    ),
    "Crash Site": LevelData(
        room_id=42,
        area_name="Alinos",
        entity_file="Unit1_C3",
    ),
    "Stronghold Void A": LevelData(
        room_id=43,
        area_name="Alinos",
        entity_file="Unit1_TP2",
    ),
    "Biodefense Chamber A": LevelData(
        room_id=44,
        area_name="Alinos",
        entity_file="Unit1_b2",
    ),
}

CELESTIAL_ARCHIVES: dict[str, LevelData] = {
    "Celestial Gateway": LevelData(
        room_id=45,
        area_name="Celestial Archives",
        entity_file="unit2_Land",
    ),
    "Helm Room": LevelData(
        room_id=46,
        area_name="Celestial Archives",
        entity_file="unit2_C0",
    ),
    "Meditation Room": LevelData(
        room_id=47,
        area_name="Celestial Archives",
        entity_file="unit2_C1",
    ),
    "Data Shrine 01": LevelData(
        room_id=48,
        area_name="Celestial Archives",
        entity_file="unit2_RM1",
    ),
    "Fan Room Alpha": LevelData(
        room_id=49,
        area_name="Celestial Archives",
        entity_file="unit2_C2",
    ),
    "Data Shrine 02": LevelData(
        room_id=50,
        area_name="Celestial Archives",
        entity_file="unit2_RM2",
    ),
    "Fan Room Beta": LevelData(
        room_id=51,
        area_name="Celestial Archives",
        entity_file="unit2_C3",
    ),
    "Data Shrine 03": LevelData(
        room_id=52,
        area_name="Celestial Archives",
        entity_file="unit2_RM3",
    ),
    "Synergy Core": LevelData(
        room_id=53,
        area_name="Celestial Archives",
        entity_file="unit2_C4",
    ),
    "Stronghold Void A": LevelData(
        room_id=54,
        area_name="Celestial Archives",
        entity_file="Unit2_TP1",
    ),
    "Biodefense Chamber A": LevelData(
        room_id=55,
        area_name="Celestial Archives",
        entity_file="Unit2_b1",
    ),
    "Tetra Vista": LevelData(
        room_id=56,
        area_name="Celestial Archives",
        entity_file="Unit2_C6",
    ),
    "New Arrival Registration": LevelData(
        room_id=57,
        area_name="Celestial Archives",
        entity_file="Unit2_C7",
    ),
    "Transfer Lock": LevelData(
        room_id=58,
        area_name="Celestial Archives",
        entity_file="Unit2_RM4",
    ),
    "Incubation Vault 01": LevelData(
        room_id=59,
        area_name="Celestial Archives",
        entity_file="Unit2_RM5",
    ),
    "Incubation Vault 02": LevelData(
        room_id=60,
        area_name="Celestial Archives",
        entity_file="Unit2_RM6",
    ),
    "Incubation Vault 03": LevelData(
        room_id=61,
        area_name="Celestial Archives",
        entity_file="Unit2_RM7",
    ),
    "Docking Bay": LevelData(
        room_id=62,
        area_name="Celestial Archives",
        entity_file="unit2_RM8",
    ),
    "Stronghold Void B": LevelData(
        room_id=63,
        area_name="Celestial Archives",
        entity_file="Unit2_TP2",
    ),
    "Biodefense Chamber B": LevelData(
        room_id=64,
        area_name="Celestial Archives",
        entity_file="Unit2_b2",
    ),
}

VESPER_DEFENSE_OUTPOST: dict[str, LevelData] = {
    "VDO Gateway": LevelData(
        room_id=65,
        area_name="Vesper Defense Outpost",
        entity_file="unit3_Land",
    ),
    "Bioweaponry Lab": LevelData(
        room_id=66,
        area_name="Vesper Defense Outpost",
        entity_file="unit3_C0",
    ),
    "Cortex CPU": LevelData(
        room_id=67,
        area_name="Vesper Defense Outpost",
        entity_file="Unit3_C2",
    ),
    "Weapons Complex": LevelData(
        room_id=68,
        area_name="Vesper Defense Outpost",
        entity_file="Unit3_RM1",
    ),
    "Compression Chamber": LevelData(
        room_id=69,
        area_name="Vesper Defense Outpost",
        entity_file="unit3_rm4",
    ),
    "Stronghold Void A": LevelData(
        room_id=70,
        area_name="Vesper Defense Outpost",
        entity_file="Unit3_TP1",
    ),
    "Biodefense Chamber A": LevelData(
        room_id=71,
        area_name="Vesper Defense Outpost",
        entity_file="Unit3_b1",
    ),
    "Ascension": LevelData(
        room_id=72,
        area_name="Vesper Defense Outpost",
        entity_file="unit3_C1",
    ),
    "Fuel Stack": LevelData(
        room_id=73,
        area_name="Vesper Defense Outpost",
        entity_file="Unit3_RM2",
    ),
    "Stasis Bunker": LevelData(
        room_id=74,
        area_name="Vesper Defense Outpost",
        entity_file="Unit3_RM3",
    ),
    "Stronghold Void B": LevelData(
        room_id=75,
        area_name="Vesper Defense Outpost",
        entity_file="Unit3_TP2",
    ),
    "Biodefense Chamber B": LevelData(
        room_id=76,
        area_name="Vesper Defense Outpost",
        entity_file="Unit3_b2",
    ),
}

ARCTERRA: dict[str, LevelData] = {
    "Arcterra Gateway": LevelData(
        room_id=77,
        area_name="Arcterra",
        entity_file="unit4_Land",
    ),
    "Ice Hive": LevelData(
        room_id=78,
        area_name="Arcterra",
        entity_file="Unit4_RM1",
    ),
    "Sic Transit": LevelData(
        room_id=79,
        area_name="Arcterra",
        entity_file="unit4_rm3",
    ),
    "Frost Labyrinth": LevelData(
        room_id=80,
        area_name="Arcterra",
        entity_file="unit4_C0",
    ),
    "Stronghold Void A": LevelData(
        room_id=81,
        area_name="Arcterra",
        entity_file="Unit4_TP1",
    ),
    "Biodefense Chamber A": LevelData(
        room_id=82,
        area_name="Arcterra",
        entity_file="unit4_b1",
    ),
    "Drip Moat": LevelData(
        room_id=83,
        area_name="Arcterra",
        entity_file="unit4_C1",
    ),
    "Subterranean": LevelData(
        room_id=84,
        area_name="Arcterra",
        entity_file="Unit4_RM2",
    ),
    "Sanctorus": LevelData(
        room_id=85,
        area_name="Arcterra",
        entity_file="unit4_rm4",
    ),
    "Fault Line": LevelData(
        room_id=86,
        area_name="Arcterra",
        entity_file="Unit4_RM5",
    ),
    "Stronghold Void B": LevelData(
        room_id=87,
        area_name="Arcterra",
        entity_file="Unit4_TP2",
    ),
    "Biodefense Chamber B": LevelData(
        room_id=88,
        area_name="Arcterra",
        entity_file="unit4_b2",
    ),
}

OUBLIETTE: dict[str, LevelData] = {
    "Oubliette Gateway": LevelData(
        room_id=89,
        area_name="Oubliette",
        entity_file="Gorea_Land",
    ),
    "Oubliette Storage": LevelData(
        room_id=90,
        area_name="Oubliette",
        entity_file="Gorea_Peek",
    ),
    "Gorea 1 Arena": LevelData(
        room_id=91,
        area_name="Oubliette",
        entity_file="Gorea_b1",
    ),
    "Gorea 2 Arena": LevelData(
        room_id=92,
        area_name="Oubliette",
        entity_file="gorea_b2",
    ),
}


def get_data(area_name: str, room_name: str) -> LevelData:
    match area_name:
        case "Alinos":
            return ALINOS[room_name]
        case "Celestial Archives":
            return CELESTIAL_ARCHIVES[room_name]
        case "Vesper Defense Outpost":
            return VESPER_DEFENSE_OUTPOST[room_name]
        case "Arcterra":
            return ARCTERRA[room_name]
        case "Oubliette":
            return OUBLIETTE[room_name]
        case _:
            return CONNECTORS[room_name]
