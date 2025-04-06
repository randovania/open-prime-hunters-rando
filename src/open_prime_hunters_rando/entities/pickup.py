from construct import Construct, Container

from open_prime_hunters_rando.constants import get_entity
from open_prime_hunters_rando.entities.entity_type import EntityType


def patch_pickups(entity_file: Construct, pickups: list) -> None:
    for pickup in pickups:
        entity_id = pickup["entity_id"]
        new_entity_type = pickup["entity_type"]
        entity_idx = get_entity(entity_file, entity_id)

        entity = entity_file.entities[entity_idx]
        header = entity.data.header

        old_entity_data = entity.data
        old_entity_type = old_entity_data.header.entity_type

        # Update ItemSpawn entities
        # Entity was ItemSpawn
        if old_entity_type == EntityType.ITEM_SPAWN:
            # Entity is still ItemSpawn
            if new_entity_type == EntityType.ITEM_SPAWN.value:
                entity.data.item_type = pickup["item_type"]
            # Entity is now Artifact
            else:
                entity.data.header.entity_type = EntityType.ARTIFACT
                entity.size = 70
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
                        "linked_entity_id": -1,
                    }
                )

        # Update Artifact Entities
        # Entity was Artifact
        else:
            # Entity is still Artifact
            if new_entity_type == EntityType.ARTIFACT.value:
                entity.data.model_id = pickup["model_id"]
                entity.data.artifact_id = pickup["artifact_id"]
            # Entity is now ItemSpawn
            else:
                entity.data.header.entity_type = EntityType.ITEM_SPAWN
                entity.size = 72
                entity.data = Container(
                    {
                        "header": header,
                        "parent_id": 65535,
                        "item_type": pickup["item_type"],
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
