from construct import Container

from open_prime_hunters_rando.entities.entity_type import EntityFile, EntityType, ItemType


def patch_pickups(entity_file: EntityFile, pickups: list) -> None:
    for pickup in pickups:
        entity_id = pickup["entity_id"]
        new_entity_type = EntityType(pickup["entity_type"])

        entity = entity_file.get_entity(entity_id)
        header = entity.data.header

        old_entity_data = entity.data
        old_entity_type = entity.entity_type

        # Update ItemSpawn entities
        # Entity was ItemSpawn
        if old_entity_type == EntityType.ITEM_SPAWN:
            # Entity is still ItemSpawn
            if new_entity_type == EntityType.ITEM_SPAWN:
                entity.data.item_type = ItemType(pickup["item_type"])
            # Entity is now Artifact
            else:
                entity.entity_type = EntityType.ARTIFACT
                entity.data = Container(
                    {
                        "header": header,
                        "model_id": pickup["model_id"],
                        "artifact_id": pickup["artifact_id"],
                        "active": old_entity_data.enabled,
                        "has_base": old_entity_data.has_base,
                        "message1_target": old_entity_data.notify_entity_id,
                        "_padding1": 0,
                        "message1": old_entity_data.collected_message,
                        "message2_target": 0,
                        "_padding2": 0,
                        "message2": 0,
                        "message3_target": 0,
                        "_padding3": 0,
                        "message3": 0,
                        "linked_entity_id": -1 if old_entity_data.parent_id == 65535 else old_entity_data.parent_id,
                    }
                )

        # Update Artifact Entities
        # Entity was Artifact
        else:
            # Entity is still Artifact
            if new_entity_type == EntityType.ARTIFACT:
                entity.data.model_id = pickup["model_id"]
                entity.data.artifact_id = pickup["artifact_id"]
            # Entity is now ItemSpawn
            else:
                entity.entity_type = EntityType.ITEM_SPAWN
                entity.data = Container(
                    {
                        "header": header,
                        "parent_id": 65535,
                        "item_type": ItemType(pickup["item_type"]),
                        "enabled": old_entity_data.active,
                        "has_base": old_entity_data.has_base,
                        "always_active": False,
                        "_padding": 0,
                        "max_spawn_count": 1,
                        "spawn_interval": 0,
                        "spawn_delay": 0,
                        "notify_entity_id": old_entity_data.message1_target,
                        "collected_message": old_entity_data.message1,
                        "collected_message_param1": 0,
                        "collected_message_param2": 0,
                    }
                )
