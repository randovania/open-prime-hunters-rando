from construct import Container

from open_prime_hunters_rando.entities.entity_type import EntityFile
from open_prime_hunters_rando.entities.enum import EntityType, ItemType


def patch_pickups(entity_file: EntityFile, pickups: list) -> None:
    for pickup in pickups:
        entity_id = pickup["entity_id"]
        new_entity_type = EntityType(pickup["entity_type"])

        entity = entity_file.get_entity(entity_id)

        old_item_spawn_data = entity.item_spawn_data()
        old_artifact_data = entity.artifact_data()
        old_entity_type = entity.entity_type

        # Update ItemSpawn entities
        # Entity was ItemSpawn
        if old_entity_type == EntityType.ITEM_SPAWN:
            # Entity is still ItemSpawn
            if new_entity_type == EntityType.ITEM_SPAWN:
                entity.item_spawn_data().item_type = ItemType(pickup["item_type"])
            # Entity is now Artifact
            else:
                entity.entity_type = EntityType.ARTIFACT
                # Raise entity so it doesn't clip into the floor
                entity.position.y += 0.3
                entity.data = Container(
                    {
                        "header": entity.header,
                        "model_id": pickup["model_id"],
                        "artifact_id": pickup["artifact_id"],
                        "active": old_item_spawn_data.enabled,
                        "has_base": old_item_spawn_data.has_base,
                        "message1_target": old_item_spawn_data.notify_entity_id,
                        "_padding1": 0,
                        "message1": old_item_spawn_data.collected_message,
                        "message2_target": 0,
                        "_padding2": 0,
                        "message2": 0,
                        "message3_target": 0,
                        "_padding3": 0,
                        "message3": 0,
                        "linked_entity_id": -1
                        if old_item_spawn_data.parent_id == 65535
                        else old_item_spawn_data.parent_id,
                    }
                )

        # Update Artifact Entities
        # Entity was Artifact
        else:
            # Entity is still Artifact
            if new_entity_type == EntityType.ARTIFACT:
                entity.artifact_data().model_id = pickup["model_id"]
                entity.artifact_data().artifact_id = pickup["artifact_id"]
            # Entity is now ItemSpawn
            else:
                entity.entity_type = EntityType.ITEM_SPAWN
                # Only lower entity if it had a base prior to avoid entity clipping into the floor in shields
                if old_artifact_data.has_base:
                    entity.position.y -= 0.3
                entity.data = Container(
                    {
                        "header": entity.header,
                        "parent_id": 65535,
                        "item_type": ItemType(pickup["item_type"]),
                        "enabled": old_artifact_data.active,
                        "has_base": old_artifact_data.has_base,
                        "always_active": False,
                        "_padding": 0,
                        "max_spawn_count": 1,
                        "spawn_interval": 0,
                        "spawn_delay": 0,
                        "notify_entity_id": old_artifact_data.message1_target,
                        "collected_message": old_artifact_data.message1,
                        "collected_message_param1": 0,
                        "collected_message_param2": 0,
                    }
                )
