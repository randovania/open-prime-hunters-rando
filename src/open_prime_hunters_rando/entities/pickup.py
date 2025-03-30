from construct import Construct

from open_prime_hunters_rando.constants import ITEM_TYPES_TO_IDS, get_entity

artifact_template = {
    "model_id": 0,
    "artifact_id": 0,
    "active": True,
    "has_base": True,
    "message1_target": 0,
    "message1": 0,
    "message2_target": 0,
    "message2": 0,
    "message3_target": 0,
    "message3": 0,
    "linked_entity_id": -1,
}


def patch_pickups(entity_file: Construct, pickups: list) -> None:
    for pickup in pickups:
        entity_id = pickup["entity_id"]
        new_entity_type = pickup["entity_type"]
        entity_idx = get_entity(entity_file, entity_id)

        entity = entity_file.entities[entity_idx]
        header = entity.data.header
        entity_data = entity.data

        new_entity_data = artifact_template

        old_entity_type = entity_data.header.entity_type

        # Update the header to use the new item type
        entity_data.header.entity_type = new_entity_type

        # Update ItemSpawn entities
        # Entity was ItemSpawn
        if old_entity_type == 4:
            # Entity is still ItemSpawn
            if new_entity_type == old_entity_type:
                entity_data.item_type = ITEM_TYPES_TO_IDS[pickup["item_type"]]
            # Entity is now Artifact
            else:
                new_entity_data["model_id"] = pickup["model_id"]
                new_entity_data["artifact_id"] = pickup["artifact_id"]
                new_entity_data["active"] = entity_data.enabled
                new_entity_data["message1_target"] = entity_data.notify_entity_id
                new_entity_data["message1"] = entity_data.collected_message

                entity.data = {
                    "header": header,
                    "model_id": pickup["model_id"],
                    "artifact_id": pickup["artifact_id"],
                    "active": new_entity_data["active"],
                    "has_base": entity_data.has_base,
                    "message1_target": new_entity_data["message1_target"],
                    "_padding1": 0x0000,
                    "message1": new_entity_data["message1"],
                    "message2_target": new_entity_data["message1_target"],
                    "_padding2": 0x0000,
                    "message2": new_entity_data["message1"],
                    "message3_target": new_entity_data["message1_target"],
                    "_padding3": 0x0000,
                    "message3": new_entity_data["message1"],
                    "linked_entity_id": -1,
                }

        # Update Artifact Entities
        # Entity was Artifact
        else:
            # Entity is still Artifact
            if new_entity_type == old_entity_type:
                entity_data.model_id = pickup["model_id"]
                entity_data.artifact_id = pickup["artifact_id"]
        #     # Entity is now ItemSpawn
        #     else:
        #         # Moving similar fields to the new fields
        #         entity_file[main_data + 20] = entity_file[main_data + 8]  # message1
        #         entity_file[main_data + 8] = entity_file[main_data + 2]  # active
        #         entity_file[main_data + 9] = entity_file[main_data + 3]  # has_base
        #         entity_file[main_data + 18] = entity_file[main_data + 4]  # message1_target

        #         # Changes to match ItemSpawn entities
        #         entity_file[main_data] = 0xFF  # Always FF
        #         entity_file[main_data + 1] = 0xFF  # Always FF
        #         entity_file[main_data + 2] = 0x00
        #         entity_file[main_data + 3] = 0x00
        #         entity_file[main_data + 4] = ITEM_TYPES_TO_IDS[pickup["item_type"]]
        #         entity_file[main_data + 5] = 0x00
        #         entity_file[main_data + 12] = 0x01  # max spawn count
        #         entity_file[main_data + 13] = 0x00
        #         entity_file[main_data + 19] = 0x00
        #         entity_file[main_data + 21] = 0x00
        #         entity_file[main_data + 28] = 0x00
        #         entity_file[main_data + 29] = 0x00
