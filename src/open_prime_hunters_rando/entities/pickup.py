from typing import TYPE_CHECKING

from open_prime_hunters_rando.entities.entity_file import EntityFile
from open_prime_hunters_rando.entities.entity_types.artifact import Artifact
from open_prime_hunters_rando.entities.entity_types.item_spawn import ItemSpawn
from open_prime_hunters_rando.entities.enum import EntityType, ItemType, Message

if TYPE_CHECKING:
    from open_prime_hunters_rando.entities.entity_type import Entity


def patch_pickups(entity_file: EntityFile, pickups: list) -> None:
    for pickup in pickups:
        entity_id = pickup["entity_id"]
        new_entity_type = EntityType(pickup["entity_type"])

        entity: Entity = entity_file.get_entity(entity_id)

        # Update ItemSpawn entities
        # Entity was ItemSpawn
        if entity.entity_type == EntityType.ITEM_SPAWN:
            assert isinstance(entity, ItemSpawn)
            # Entity is still ItemSpawn
            if new_entity_type == EntityType.ITEM_SPAWN:
                entity.item_type = ItemType(pickup["item_type"])
            else:
                # Entity is now Artifact
                entity_file.replace_entity(
                    entity_id,
                    Artifact.create(
                        position=entity.position,
                        up_vector=entity.up_vector,
                        facing_vector=entity.facing_vector,
                        model_id=pickup["model_id"],
                        artifact_id=pickup["artifact_id"],
                        active=entity.enabled,
                        has_base=entity.has_base,
                        message1_target=entity.notify_entity_id,
                        message1=entity.collected_message,
                        message2_target=0,
                        message2=Message.NONE,
                        message3_target=0,
                        message3=Message.NONE,
                        linked_entity_id=-1 if entity.parent_id == 65535 else entity.parent_id,
                    ),
                )
        # Update Artifact Entities
        # Entity was Artifact
        else:
            assert isinstance(entity, Artifact)
            # Entity is still Artifact
            if new_entity_type == EntityType.ARTIFACT:
                entity.model_id = pickup["model_id"]
                entity.artifact_id = pickup["artifact_id"]
            else:
                # Entity is now ItemSpawn
                # Only lower entity if it had a base prior to avoid entity clipping into the floor in shields
                if entity.has_base:
                    entity.position.y -= 0.3
                entity_file.replace_entity(
                    entity_id,
                    ItemSpawn.create(
                        position=entity.position,
                        up_vector=entity.up_vector,
                        facing_vector=entity.facing_vector,
                        parent_id=65535,
                        item_type=ItemType(pickup["item_type"]),
                        enabled=entity.active,
                        has_base=entity.has_base,
                        always_active=False,
                        max_spawn_count=1,
                        spawn_interval=0,
                        spawn_delay=0,
                        notify_entity_id=entity.message1_target,
                        collected_message=entity.message1,
                        collected_message_param1=0,
                        collected_message_param2=0,
                    ),
                )
