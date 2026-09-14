from typing import TYPE_CHECKING, TypedDict

from open_prime_hunters_rando.parsing.formats.entities.entity_file import EntityFile
from open_prime_hunters_rando.parsing.formats.entities.entity_types.artifact import Artifact, ModelId
from open_prime_hunters_rando.parsing.formats.entities.entity_types.item_spawn import ItemSpawn
from open_prime_hunters_rando.parsing.formats.entities.entity_types.trigger_volume import (
    TriggerVolume,
    TriggerVolumeType,
)
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType, ItemType, Message
from open_prime_hunters_rando.patching.entities.state_bits import get_state_bit

if TYPE_CHECKING:
    from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity


class PickupProperties(TypedDict):
    entity_id: int
    entity_type: int
    item_type: int
    state_bit: int
    artifact_id: int
    model_id: int


def patch_pickups(entity_file: EntityFile, pickups: list[PickupProperties], room_name: str) -> None:
    if room_name == "High Ground":
        _update_high_ground_big_health_layers(entity_file)

    for pickup in pickups:
        _patch_pickup(entity_file, pickup, room_name)


def _patch_pickup(entity_file: EntityFile, pickup: PickupProperties, room_name: str) -> None:
    entity_id = pickup["entity_id"]
    new_entity_type = EntityType(pickup["entity_type"])

    entity: Entity = entity_file.get_entity(entity_id)
    new_entity: Entity

    # Update ItemSpawn entities
    # Entity was ItemSpawn
    if isinstance(entity, ItemSpawn):
        # Entity is still ItemSpawn
        if new_entity_type == EntityType.ITEM_SPAWN:
            new_item_type = ItemType(pickup["item_type"])

            if entity.item_type == ItemType.ARTIFACT_KEY != new_item_type:
                _remove_shield_key_messages(entity)

            entity.item_type = new_item_type

            if new_item_type == ItemType.ARTIFACT_KEY:
                _add_shield_key_pickup_trigger(entity_file, None, entity, pickup["state_bit"], room_name)

        # Entity is now Artifact
        else:
            # Raise entity so it doesn't clip into the floor if not an Octolith
            if ModelId(pickup["model_id"]) != ModelId.OCTOLITH:
                entity.position.y += 0.3
            else:
                _adjust_octolith_positions(entity, room_name)

            if entity.collected_message == Message.SET_TRIGGER_STATE:
                _remove_shield_key_messages(entity)

            new_entity = Artifact.create(
                position=entity.position,
                model_id=ModelId(pickup["model_id"]),
                artifact_id=pickup["artifact_id"],
                active=entity.enabled,
                # Octoliths do not have a base and will crash if "has_base" is true
                has_base=entity.has_base if ModelId(pickup["model_id"]) != ModelId.OCTOLITH else False,
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
            entity.model_id = ModelId(pickup["model_id"])
            entity.artifact_id = pickup["artifact_id"]

            # Octoliths do not have a base and will crash if "has_base" is true
            if entity.model_id == ModelId.OCTOLITH:
                # For Artifact locations that are not in a shield, lower the Octolith and remove the base
                if entity.has_base:
                    entity.position.y -= 0.5
                    entity.has_base = False
                else:
                    _adjust_octolith_positions(entity, room_name)

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
                _add_shield_key_pickup_trigger(entity_file, entity, new_entity, pickup["state_bit"], room_name)

            entity_file.replace_entity(entity_id, new_entity)


def _remove_shield_key_messages(entity: ItemSpawn) -> None:
    # Removes inherited messages from the entity if it is no longer a Shield Key
    entity.notify_entity_id = -1
    entity.collected_message = Message.NONE
    entity.collected_message_param1 = 0


def _add_shield_key_pickup_trigger(
    entity_file: EntityFile, artifact_entity: Artifact | None, new_entity: ItemSpawn, state_bit: int, room_name: str
) -> None:
    # Adds a new trigger if the Shield Key replaced an Artifact which sets the state bit and sends any other messages
    if artifact_entity is not None:
        artifact_trigger = TriggerVolume.create(
            node_name=new_entity.node_name,
            layer_state=new_entity.layer_state,
            subtype=TriggerVolumeType.AUTOMATIC,
            active=False,
            always_active=False,
            parent_id=new_entity.notify_entity_id,
            parent_message=new_entity.collected_message,
            parent_message_param1=new_entity.collected_message_param1,
            parent_message_param2=new_entity.collected_message_param2,
            child_message=Message.SET_TRIGGER_STATE,
            child_message_param1=state_bit,
        )
        entity_file.append_entity(artifact_trigger)

        # The Shield Key will activate the new trigger
        new_entity.notify_entity_id = artifact_trigger.entity_id
        new_entity.collected_message = Message.ACTIVATE

    else:
        # Updates the message and state bit set by the shield key based on the configuration
        new_entity.collected_message = Message.SET_TRIGGER_STATE
        new_entity.collected_message_param1 = state_bit

    # Create a new trigger volume to show the message and play the sfx if the new Shield Key is not vanilla
    vanilla_shield_key = get_state_bit(state_bit)
    if vanilla_shield_key.entity_id != new_entity.entity_id or vanilla_shield_key.room_name != room_name:
        # First Shield Key message has a string_id of 56
        # 24 is added to the message_id because the first custom state bit is 32
        message_id = state_bit + 24

        # Create new trigger volume
        key_trigger = TriggerVolume.create(
            node_name=new_entity.node_name,
            layer_state=new_entity.layer_state,
            subtype=TriggerVolumeType.STATE_BITS,
            always_active=False,
            required_state_bit=state_bit,
            parent_message=Message.SHOW_PROMPT,
            parent_message_param1=message_id,
            child_message=Message.PLAY_SFX_SCRIPT,
            child_message_param1=19,
        )
        entity_file.append_entity(key_trigger)


def _adjust_octolith_positions(entity: ItemSpawn, room_name: str) -> None:
    # Adjust the height of Octoliths on a room by room basis
    rooms_with_height_adjustments: dict[list[tuple[int, float]]] = {
        "Cortex CPU": [(18, 1.6)],
        "Compression Chamber": [(9, 1.1)],
        "Council Chamber": [(19, 2.0)],
        "Data Shrine 01": [(14, 1.2), (55, 1.2), (57, 1.4)],
        "Data Shrine 02": [(15, 1.4), (18, 1.1)],
        "Echo Hall": [(15, 1.0), (42, 1.0)],
        "Elder Passage": [(29, 0.9)],
        "Fault Line": [(47, 0.6)],
        "Frost Labyrinth": [(18, 0.6)],
        "High Ground": [(59, 1.6)],
        "Sic Transit": [(29, 0.5)],
    }

    entity_ids = rooms_with_height_adjustments.get(room_name, None)
    if entity_ids is not None:
        for entity_id, adjustment in entity_ids:
            if entity.entity_id == entity_id:
                entity.position.y -= adjustment
            break

    # Move the Zoomers pickup away from the wall
    if room_name == "Echo Hall" and entity.entity_id == 42:
        entity.position.z += 0.3
    # Move the small room pickups away from the walls
    if room_name == "Data Shrine 03":
        if entity.entity_id == 2:
            entity.position.z -= 0.1
        elif entity.entity_id == 46:
            entity.position.x -= 0.2


def _update_high_ground_big_health_layers(high_ground: EntityFile) -> None:
    big_health = high_ground.get_entity(59, ItemSpawn)
    for layer in range(4):
        big_health.layer_state[layer] = True
