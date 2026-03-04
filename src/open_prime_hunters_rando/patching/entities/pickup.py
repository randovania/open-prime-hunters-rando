from typing import TYPE_CHECKING

from open_prime_hunters_rando.parsing.formats.entities.entity_file import EntityFile
from open_prime_hunters_rando.parsing.formats.entities.entity_types.artifact import Artifact
from open_prime_hunters_rando.parsing.formats.entities.entity_types.item_spawn import ItemSpawn
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType, ItemType

if TYPE_CHECKING:
    from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity


def patch_pickups(entity_file: EntityFile, pickups: list) -> None:
    for pickup in pickups:
        entity_id = pickup["entity_id"]
        new_entity_type = EntityType(pickup["entity_type"])

        entity: Entity = entity_file.get_entity(entity_id)
        new_entity: Entity

        # Update ItemSpawn entities
        # Entity was ItemSpawn
        if isinstance(entity, ItemSpawn):
            # Entity is still ItemSpawn
            if new_entity_type == EntityType.ITEM_SPAWN:
                entity.item_type = ItemType(pickup["item_type"])

            # Entity is now Artifact
            else:
                # Raise entity so it doesn't clip into the floor
                entity.position.y += 0.3

                new_entity = Artifact.create(
                    model_id=pickup["model_id"],
                    artifact_id=pickup["artifact_id"],
                    active=entity.enabled,
                    has_base=entity.has_base,
                    message1_target=entity.notify_entity_id,
                    message1=entity.collected_message,
                    linked_entity_id=(-1 if entity.parent_id == 65535 else entity.parent_id),
                )

                entity_file.replace_entity(entity_id, new_entity)

        # Update Artifact Entities
        # Entity was Artifact
        else:
            assert isinstance(entity, Artifact)

            # Entity is still Artifact
            if new_entity_type == EntityType.ARTIFACT:
                entity.model_id = pickup["model_id"]
                entity.artifact_id = pickup["artifact_id"]

            # Entity is now ItemSpawn
            else:
                # Only lower entity if it had a base prior to avoid entity clipping into the floor in shields
                if entity.has_base:
                    entity.position.y -= 0.3

                new_entity = ItemSpawn.create(
                    item_type=ItemType(pickup["item_type"]),
                    enabled=entity.active,
                    has_base=entity.has_base,
                    notify_entity_id=entity.message1_target,
                    collected_message=entity.message1,
                )

                entity_file.replace_entity(entity_id, new_entity)
