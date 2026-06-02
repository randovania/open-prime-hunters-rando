from typing import TYPE_CHECKING

from open_prime_hunters_rando.parsing.common_types.volume import SphereVolumeType, TriggerVolumeFlags
from open_prime_hunters_rando.parsing.formats.entities.entity_file import EntityFile
from open_prime_hunters_rando.parsing.formats.entities.entity_types.artifact import Artifact
from open_prime_hunters_rando.parsing.formats.entities.entity_types.item_spawn import ItemSpawn
from open_prime_hunters_rando.parsing.formats.entities.entity_types.trigger_volume import (
    TriggerVolume,
    TriggerVolumeType,
)
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType, ItemType, Message

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
                new_entity = ItemSpawn.create(
                    layer_state=entity.layer_state,
                    position=entity.position,
                    item_type=ItemType(pickup["item_type"]),
                    enabled=entity.enabled,
                    has_base=entity.has_base,
                )

                # Removes inherited messages from ItemSpawns that replaced the Shield Key
                if entity.item_type == ItemType.ARTIFACT_KEY != new_entity.item_type:
                    new_entity.collected_message = Message.NONE

                if new_entity.item_type == ItemType.ARTIFACT_KEY:
                    _add_shield_key_trigger(entity_file, new_entity, pickup["state_bit"])

                entity_file.replace_entity(entity_id, new_entity)

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
                    node_name=entity.node_name,
                    layer_state=entity.layer_state,
                    position=entity.position,
                    item_type=ItemType(pickup["item_type"]),
                    enabled=entity.active,
                    has_base=entity.has_base,
                    notify_entity_id=entity.message1_target,
                    collected_message=entity.message1,
                )

                if new_entity.item_type == ItemType.ARTIFACT_KEY:
                    _add_shield_key_trigger(entity_file, new_entity, pickup["state_bit"])

                entity_file.replace_entity(entity_id, new_entity)


def _add_shield_key_trigger(entity_file: EntityFile, new_entity: ItemSpawn, state_bit: int) -> None:
    # First Shield Key message has a string_id of 57
    # 25 is added to the message_id because the first custom state bit is 32
    message_id = state_bit + 25

    # Create a new trigger volume to show the message and play the sfx
    key_trigger = TriggerVolume.create(
        node_name=new_entity.node_name,
        position=new_entity.position,
        layer_state=new_entity.layer_state,
        subtype=TriggerVolumeType.VOLUME,
        volume=SphereVolumeType.create(),
        trigger_flags=TriggerVolumeFlags.PLAYER_BIPED | TriggerVolumeFlags.PLAYER_ALT,
        parent_message=Message.SHOW_PROMPT,
        parent_message_param1=message_id,
        child_message=Message.PLAY_SFX_SCRIPT,
        child_message_param1=19,
    )
    entity_file.append_entity(key_trigger)

    # Sets a custom state bit when picked up which is activates its corresponding recipient
    new_entity.notify_entity_id = -1
    new_entity.collected_message = Message.SET_TRIGGER_STATE
    new_entity.collected_message_param1 = state_bit
