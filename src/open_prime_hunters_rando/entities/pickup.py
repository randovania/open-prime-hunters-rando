from open_prime_hunters_rando.constants import ITEM_TYPES_TO_IDS, get_entity


def patch_pickups(entity_file: memoryview, pickups: list) -> None:
    for pickup in pickups:
        entity_id = pickup["entity_id"]
        new_entity_type = pickup["entity_type"]

        data_offset, old_entity_type = get_entity(entity_file, entity_id)

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
                entity_file[main_data + 5] = 0x00
                entity_file[main_data + 12] = 0x01  # max spawn count
                entity_file[main_data + 13] = 0x00
                entity_file[main_data + 19] = 0x00
                entity_file[main_data + 21] = 0x00
                entity_file[main_data + 28] = 0x00
                entity_file[main_data + 29] = 0x00
