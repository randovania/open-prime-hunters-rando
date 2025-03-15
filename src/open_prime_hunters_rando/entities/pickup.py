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


def _get_entity(entity_file: memoryview, entity_id: int) -> tuple[int, int]:
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
        if found_entity_id != entity_id:
            entry_start += entry_length
            entry_end += entry_length
            i += 1
        else:
            break

    return data_offset, found_entity_type


def patch_pickups(entity_file: memoryview, pickups: list) -> None:
    for pickup in pickups:
        entity_id = pickup["entity_id"]
        new_entity_type = pickup["entity_type"]

        data_offset, old_entity_type = _get_entity(entity_file, entity_id)

        # Update the header to use the new item type
        entity_file[data_offset] = new_entity_type

        # Entity Data is offset 0x28 (40) from the start of the header
        main_data = data_offset + 40

        # Update ItemSpawn entities
        # Entity was ItemSpawn
        if old_entity_type == 4:
            # Entity is still ItemSpawn
            if new_entity_type == old_entity_type:
                entity_file[main_data + 4] = ITEM_TYPES_TO_IDS[pickup["item_type"]]
            # Entity is now Artifact
            else:
                # Moving similar fields to the new offsets
                entity_file[main_data + 2] = entity_file[main_data + 8]  # active
                entity_file[main_data + 3] = entity_file[main_data + 9]  # has_base
                entity_file[main_data + 4] = entity_file[main_data + 18]  # notify_entity_id
                entity_file[main_data + 8] = entity_file[main_data + 20]  # collected_message

                # Changes to match Artifact entities
                entity_file[main_data] = pickup["model_id"]
                entity_file[main_data + 1] = pickup["artifact_id"]
                entity_file[main_data + 5] = 0xFF
                entity_file[main_data + 9] = 0x00
                entity_file[main_data + 12] = 0xFF  # Always FF
                entity_file[main_data + 13] = 0xFF  # Always FF
                entity_file[main_data + 18] = 0x00
                entity_file[main_data + 19] = 0x00
                entity_file[main_data + 20] = 0xFF  # Always FF
                entity_file[main_data + 21] = 0xFF  # Always FF

        # Update Artifact Entities
        # Entity was Artifact
        else:
            # Entity is still Artifact
            if new_entity_type == old_entity_type:
                entity_file[main_data] = pickup["model_id"]
                entity_file[main_data + 1] = pickup["artifact_id"]
            # Entity is now ItemSpawn
            else:
                # Moving similar fields to the new offsets
                entity_file[main_data + 20] = entity_file[main_data + 8]  # message1
                entity_file[main_data + 8] = entity_file[main_data + 2]  # active
                entity_file[main_data + 9] = entity_file[main_data + 3]  # has_base
                entity_file[main_data + 18] = entity_file[main_data + 4]  # message1_target

                # Changes to match ItemSpawn entities
                entity_file[main_data] = 0xFF  # Always FF
                entity_file[main_data + 1] = 0xFF  # Always FF
                entity_file[main_data + 2] = 0x00
                entity_file[main_data + 3] = 0x00
                entity_file[main_data + 4] = ITEM_TYPES_TO_IDS[pickup["item_type"]]
                entity_file[main_data + 12] = 0x01  # max spawn count
                entity_file[main_data + 13] = 0x00
                entity_file[main_data + 19] = 0x00
                entity_file[main_data + 21] = 0x00
                entity_file[main_data + 28] = 0x00
                entity_file[main_data + 29] = 0x00
