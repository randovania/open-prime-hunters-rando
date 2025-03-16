ITEM_TYPES_TO_IDS = {
    "HealthMedium": 0,
    "HealthSmall": 1,
    "HealthBig": 2,
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
    "UAExpansion": 18,
    "ArtifactKey": 19,
}


def get_entity(entity_file: memoryview, new_entity_id: int) -> tuple[int, int]:
    num_entities = entity_file[0x04]
    entry_length = 0x18

    i = 1
    entry_start = 0x24
    entry_end = 0x3C
    while i <= num_entities:
        entity_entry = entity_file[entry_start:entry_end]
        data_offset = int.from_bytes(entity_entry[0x14:0x16], "little")
        found_entity_type = entity_file[data_offset]
        found_entity_id = entity_file[data_offset + 2]
        if found_entity_id != new_entity_id:
            entry_start += entry_length
            entry_end += entry_length
            i += 1
        else:
            break

    return data_offset, found_entity_type
