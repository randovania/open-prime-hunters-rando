from ndspy.rom import NintendoDSRom

ITEM_TYPES_TO_IDS = {
    "None": -1,
    "HealthMedium": 0,
    "HealthSmall": 1,
    "HealthBig": 2,
    "DoubleDamage": 3,
    "EnergyTank": 4,
    "VoltDriver": 5,
    "MissileExpansion": 6,
    "Battlehammer": 7,
    "Imperialist": 8,
    "Judicator": 9,
    "Magmaul": 10,
    "ShockCoil": 11,
    "OmegaCannon": 12,
    "UASmall": 13,
    "UABig": 14,
    "MissileSmall": 15,
    "MissileBig": 16,
    "Cloak": 17,
    "UAExpansion": 18,
    "ArtifactKey": 19,
    "Deathalt": 20,
    "AffinityWeapon": 21,
    "PickWpnMissile": 22,
}


ENTITY_FILES = {
    # Celestial Archives
    "Celestial Gateway": "unit2_Land",
    "Biodefense Chamber 01": "Unit2_b1",
    "Biodefense Chamber 05": "Unit2_b2",
    "Data Shrine 01": "unit2_RM1",
    "Data Shrine 02": "unit2_RM2",
    "Data Shrine 03": "unit2_RM3",
    "Docking Bay": "Unit2_RM8",
    "Incubation Vault 01": "unit2_RM5",
    "Incubation Vault 02": "unit2_RM6",
    "Incubation Vault 03": "Unit2_RM7",
    "New Arrival Registration": "Unit2_C7",
    "Synergy Core": "unit2_C4",
    "Transfer Lock": "Unit2_RM4",
    # Alinos
    "Alinos Gateway": "Unit1_Land",
    "Alinos Perch": "unit1_RM2",
    "Biodefense Chamber 02": "Unit1_b1",
    "Biodefense Chamber 06": "Unit1_b2",
    "Council Chamber": "unit1_rm3",
    "Crash Site": "Unit1_C3",
    "Echo Hall": "Unit1_C0",
    "Elder Passage": "unit_RM6",
    "High Ground": "unit1_RM1",
    "Magma Drop": "Unit1_C4",
    "Piston Cave": "Unit1_C5",
    "Processor Core": "unit1_rm5",
    # Arcterra
    "Biodefense Chamber 04": "Unit1_b1",
    "Biodefense Chamber 07": "Unit1_b2",
    "Drip Moat": "unit4_C1",
    "Fault Line": "Unit4_RM5",
    "Frost Labyrinth": "unit4_C0",
    "Ice Hive": "Unit4_RM1",
    "Sanctorus": "unit4_rm4",
    "Sic Transit": "unit4_rm3",
    "Subterranean": "Unit4_RM2",
    # Vesper Defense Outpost
    "Biodefense Chamber 03": "Unit1_b1",
    "Biodefense Chamber 08": "Unit1_b2",
    "Compression Chamber": "unit3_rm4",
    "Cortex CPU": "Unit3_C2",
    "Fuel Stack": "Unit3_RM2",
    "Stasis Bunker": "Unit3_RM3",
    "Weapons Complex": "Unit3_RM1",
    # Oubliette
    "Gorea Peek": "Gorea_Peek",
}


def patch_pickups(rom: NintendoDSRom, configuration: dict[str, dict]) -> None:
    for area_name, area_config in configuration.items():
        for level_name, level_config in area_config.items():
            for room_name, room_config in level_config.items():
                # Load the entity file
                entity_file = rom.getFileByName(f"levels/entities/{ENTITY_FILES[room_name]}_Ent.bin")
                mv = memoryview(entity_file)
                for pickup in room_config["pickups"]:
                    # Modify the value at the specified offset to edit the ItemType
                    offset = pickup["entity_offset"]
                    item_type = ITEM_TYPES_TO_IDS[pickup["item_type"]]
                    mv[offset] = item_type
