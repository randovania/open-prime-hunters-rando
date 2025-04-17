import dataclasses

from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.entities.entity_type import EntityFile


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
        entity_file="Unit1_Land_Ent",
    ),
    "Echo Hall": LevelData(
        room_id=28,
        area_name="Alinos",
        entity_file="Unit1_C0_Ent",
    ),
    "High Ground": LevelData(
        room_id=29,
        area_name="Alinos",
        entity_file="unit1_RM1_Ent",
    ),
    "Magma Drop": LevelData(
        room_id=30,
        area_name="Alinos",
        entity_file="Unit1_C4_Ent",
    ),
    "Elder Passage": LevelData(
        room_id=31,
        area_name="Alinos",
        entity_file="unit1_RM6_Ent",
    ),
    "Alimbic Cannon Control Room": LevelData(
        room_id=32,
        area_name="Alinos",
        entity_file="crystalroom_Ent",
    ),
    "Combat Hall": LevelData(
        room_id=33,
        area_name="Alinos",
        entity_file="unit1_rm4_Ent",
    ),
    "Stronghold Void B": LevelData(
        room_id=34,
        area_name="Alinos",
        entity_file="Unit1_TP1_Ent",
    ),
    "Biodefense Chamber B": LevelData(
        room_id=35,
        area_name="Alinos",
        entity_file="Unit1_b1_Ent",
    ),
    "Alimbic Gardens": LevelData(
        room_id=36,
        area_name="Alinos",
        entity_file="Unit1_C1_Ent",
    ),
    "Thermal Vast": LevelData(
        room_id=37,
        area_name="Alinos",
        entity_file="Unit1_C2_Ent",
    ),
    "Piston Cave": LevelData(
        room_id=38,
        area_name="Alinos",
        entity_file="Unit1_C5_Ent",
    ),
    "Alinos Perch": LevelData(
        room_id=39,
        area_name="Alinos",
        entity_file="unit1_RM2_ent",
    ),
    "Council Chamber": LevelData(
        room_id=40,
        area_name="Alinos",
        entity_file="unit1_rm3_Ent",
    ),
    "Processor Core": LevelData(
        room_id=41,
        area_name="Alinos",
        entity_file="unit1_rm5_Ent",
    ),
    "Crash Site": LevelData(
        room_id=42,
        area_name="Alinos",
        entity_file="Unit1_C3_Ent",
    ),
    "Stronghold Void A": LevelData(
        room_id=43,
        area_name="Alinos",
        entity_file="Unit1_TP2_Ent",
    ),
    "Biodefense Chamber A": LevelData(
        room_id=44,
        area_name="Alinos",
        entity_file="Unit1_b2_Ent",
    ),
}

CELESTIAL_ARCHIVES: dict[str, LevelData] = {
    "Celestial Gateway": LevelData(
        room_id=45,
        area_name="Celestial Archives",
        entity_file="unit2_Land_Ent",
    ),
    "Helm Room": LevelData(
        room_id=46,
        area_name="Celestial Archives",
        entity_file="unit2_C0_Ent",
    ),
    "Meditation Room": LevelData(
        room_id=47,
        area_name="Celestial Archives",
        entity_file="unit2_C1_Ent",
    ),
    "Data Shrine 01": LevelData(
        room_id=48,
        area_name="Celestial Archives",
        entity_file="unit2_RM1_Ent",
    ),
    "Fan Room Alpha": LevelData(
        room_id=49,
        area_name="Celestial Archives",
        entity_file="unit2_C2_Ent",
    ),
    "Data Shrine 02": LevelData(
        room_id=50,
        area_name="Celestial Archives",
        entity_file="unit2_RM2_Ent",
    ),
    "Fan Room Beta": LevelData(
        room_id=51,
        area_name="Celestial Archives",
        entity_file="unit2_C3_Ent",
    ),
    "Data Shrine 03": LevelData(
        room_id=52,
        area_name="Celestial Archives",
        entity_file="unit2_RM3_Ent",
    ),
    "Synergy Core": LevelData(
        room_id=53,
        area_name="Celestial Archives",
        entity_file="unit2_C4_Ent",
    ),
    "Stronghold Void A": LevelData(
        room_id=54,
        area_name="Celestial Archives",
        entity_file="Unit2_TP1_Ent",
    ),
    "Biodefense Chamber A": LevelData(
        room_id=55,
        area_name="Celestial Archives",
        entity_file="Unit2_b1_Ent",
    ),
    "Tetra Vista": LevelData(
        room_id=56,
        area_name="Celestial Archives",
        entity_file="Unit2_C6_Ent",
    ),
    "New Arrival Registration": LevelData(
        room_id=57,
        area_name="Celestial Archives",
        entity_file="Unit2_C7_Ent",
    ),
    "Transfer Lock": LevelData(
        room_id=58,
        area_name="Celestial Archives",
        entity_file="Unit2_RM4_Ent",
    ),
    "Incubation Vault 01": LevelData(
        room_id=59,
        area_name="Celestial Archives",
        entity_file="Unit2_RM5_Ent",
    ),
    "Incubation Vault 02": LevelData(
        room_id=60,
        area_name="Celestial Archives",
        entity_file="Unit2_RM6_Ent",
    ),
    "Incubation Vault 03": LevelData(
        room_id=61,
        area_name="Celestial Archives",
        entity_file="Unit2_RM7_Ent",
    ),
    "Docking Bay": LevelData(
        room_id=62,
        area_name="Celestial Archives",
        entity_file="unit2_RM8_Ent",
    ),
    "Stronghold Void B": LevelData(
        room_id=63,
        area_name="Celestial Archives",
        entity_file="Unit2_TP2_Ent",
    ),
    "Biodefense Chamber B": LevelData(
        room_id=64,
        area_name="Celestial Archives",
        entity_file="Unit2_b2_Ent",
    ),
}

VESPER_DEFENSE_OUTPOST: dict[str, LevelData] = {
    "VDO Gateway": LevelData(
        room_id=65,
        area_name="Vesper Defense Outpost",
        entity_file="unit3_Land_Ent",
    ),
    "Bioweaponry Lab": LevelData(
        room_id=66,
        area_name="Vesper Defense Outpost",
        entity_file="unit3_C0_Ent",
    ),
    "Cortex CPU": LevelData(
        room_id=67,
        area_name="Vesper Defense Outpost",
        entity_file="Unit3_C2_Ent",
    ),
    "Weapons Complex": LevelData(
        room_id=68,
        area_name="Vesper Defense Outpost",
        entity_file="Unit3_RM1_Ent",
    ),
    "Compression Chamber": LevelData(
        room_id=69,
        area_name="Vesper Defense Outpost",
        entity_file="unit3_rm4_Ent",
    ),
    "Stronghold Void A": LevelData(
        room_id=70,
        area_name="Vesper Defense Outpost",
        entity_file="Unit3_TP1_Ent",
    ),
    "Biodefense Chamber A": LevelData(
        room_id=71,
        area_name="Vesper Defense Outpost",
        entity_file="Unit3_b1_Ent",
    ),
    "Ascension": LevelData(
        room_id=72,
        area_name="Vesper Defense Outpost",
        entity_file="unit3_C1_Ent",
    ),
    "Fuel Stack": LevelData(
        room_id=73,
        area_name="Vesper Defense Outpost",
        entity_file="Unit3_RM2_Ent",
    ),
    "Stasis Bunker": LevelData(
        room_id=74,
        area_name="Vesper Defense Outpost",
        entity_file="Unit3_RM3_Ent",
    ),
    "Stronghold Void B": LevelData(
        room_id=75,
        area_name="Vesper Defense Outpost",
        entity_file="Unit3_TP2_Ent",
    ),
    "Biodefense Chamber B": LevelData(
        room_id=76,
        area_name="Vesper Defense Outpost",
        entity_file="Unit3_b2_Ent",
    ),
}

ARCTERRA: dict[str, LevelData] = {
    "Arcterra Gateway": LevelData(
        room_id=77,
        area_name="Arcterra",
        entity_file="unit4_Land_Ent",
    ),
    "Ice Hive": LevelData(
        room_id=78,
        area_name="Arcterra",
        entity_file="Unit4_RM1_Ent",
    ),
    "Sic Transit": LevelData(
        room_id=79,
        area_name="Arcterra",
        entity_file="unit4_rm3_Ent",
    ),
    "Frost Labyrinth": LevelData(
        room_id=80,
        area_name="Arcterra",
        entity_file="unit4_C0_Ent",
    ),
    "Stronghold Void A": LevelData(
        room_id=81,
        area_name="Arcterra",
        entity_file="Unit4_TP1_Ent",
    ),
    "Biodefense Chamber A": LevelData(
        room_id=82,
        area_name="Arcterra",
        entity_file="unit4_b1_Ent",
    ),
    "Drip Moat": LevelData(
        room_id=83,
        area_name="Arcterra",
        entity_file="unit4_C1_Ent",
    ),
    "Subterranean": LevelData(
        room_id=84,
        area_name="Arcterra",
        entity_file="Unit4_RM2_Ent",
    ),
    "Sanctorus": LevelData(
        room_id=85,
        area_name="Arcterra",
        entity_file="unit4_rm4_Ent",
    ),
    "Fault Line": LevelData(
        room_id=86,
        area_name="Arcterra",
        entity_file="Unit4_RM5_Ent",
    ),
    "Stronghold Void B": LevelData(
        room_id=87,
        area_name="Arcterra",
        entity_file="Unit4_TP2_Ent",
    ),
    "Biodefense Chamber B": LevelData(
        room_id=88,
        area_name="Arcterra",
        entity_file="unit4_b2_Ent",
    ),
}

OUBLIETTE: dict[str, LevelData] = {
    "Oubliette Gateway": LevelData(
        room_id=89,
        area_name="Oubliette",
        entity_file="Gorea_Land_Ent",
    ),
    "Oubliette Storage": LevelData(
        room_id=90,
        area_name="Oubliette",
        entity_file="Gorea_Peek_Ent",
    ),
    "Gorea 1 Arena": LevelData(
        room_id=91,
        area_name="Oubliette",
        entity_file="Gorea_b1_Ent",
    ),
    "Gorea 2 Arena": LevelData(
        room_id=92,
        area_name="Oubliette",
        entity_file="gorea_b2_Ent",
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


def get_entity_file(rom: NintendoDSRom, area_name: str, room_name: str) -> tuple[str, EntityFile]:
    level_data = get_data(area_name, room_name)
    file_name = f"levels/entities/{level_data.entity_file}.bin"
    parsed_file = EntityFile.parse(rom.getFileByName(file_name))

    return file_name, parsed_file
