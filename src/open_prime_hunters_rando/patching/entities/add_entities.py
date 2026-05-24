import copy
from typing import TYPE_CHECKING, NamedTuple

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3
from open_prime_hunters_rando.parsing.common_types.volume import SphereVolumeType, TriggerVolumeFlags
from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.parsing.formats.entities.entity_types.item_spawn import ItemSpawn
from open_prime_hunters_rando.parsing.formats.entities.entity_types.object import Object
from open_prime_hunters_rando.parsing.formats.entities.entity_types.trigger_volume import TriggerVolume
from open_prime_hunters_rando.parsing.formats.entities.enum import ItemType, Message
from open_prime_hunters_rando.patching.entities import NewTrigger

if TYPE_CHECKING:
    from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity


def add_new_entities(file_manager: FileManager, new_artifact_triggers: list[NewTrigger]) -> None:
    # Creates a new entity of a given EntityType from provided lists
    _add_new_triggers(file_manager, new_artifact_triggers)
    for new_object in new_objects:
        _add_new_objects(file_manager, new_object)


new_triggers: list[NewTrigger] = []


def _add_new_triggers(file_manager: FileManager, new_artifact_triggers: list[NewTrigger]) -> None:
    # Add all generated artifact triggers to the main list of new triggers
    new_triggers.extend(new_artifact_triggers)

    for new_trigger in new_triggers:
        entity_file = file_manager.get_entity_file(new_trigger.area_name, new_trigger.room_name)
        item_spawn: Entity = entity_file.get_entity(new_trigger.entity_id)

        # Only add new triggers if the entity is an ItemSpawn
        if not isinstance(item_spawn, ItemSpawn):
            continue

        template_trigger = TriggerVolume.create(
            node_name=new_trigger.node_name,
            layer_state=item_spawn.layer_state,
            position=item_spawn.position,
            volume=SphereVolumeType.create(),
            active=False,
            trigger_flags=TriggerVolumeFlags.PLAYER_BIPED | TriggerVolumeFlags.PLAYER_ALT,
        )

        # Get the new trigger
        trigger_volume_a = entity_file.get_entity(entity_file.append_entity(template_trigger), TriggerVolume)

        # Update the ItemSpawn to activate the trigger
        if item_spawn.item_type == ItemType.ARTIFACT_KEY:
            key_trigger = TriggerVolume.create(
                node_name=item_spawn.node_name,
                layer_state=item_spawn.layer_state,
                position=item_spawn.position,
                volume=template_trigger.volume,
                active=False,
                trigger_flags=TriggerVolumeFlags.PLAYER_BIPED | TriggerVolumeFlags.PLAYER_ALT,
                parent_id=trigger_volume_a.entity_id,
                parent_message=Message.ACTIVATE,
                child_id=item_spawn.notify_entity_id,
                child_message=item_spawn.collected_message,
                child_message_param1=item_spawn.collected_message_param1,
            )
            entity_file.append_entity(key_trigger)

            item_spawn.notify_entity_id = key_trigger.entity_id
            item_spawn.collected_message_param1 = 0
        else:
            item_spawn.notify_entity_id = trigger_volume_a.entity_id

        item_spawn.collected_message = Message.ACTIVATE

        # Send the first message from the Artifact
        trigger_volume_a.parent_id = new_trigger.artifact_messages[0][0]
        trigger_volume_a.parent_message = new_trigger.artifact_messages[0][1]

        num_messages = len(new_trigger.artifact_messages)

        if num_messages == 2:
            # Send the second message from the Artifact
            trigger_volume_a.child_id = new_trigger.artifact_messages[1][0]
            trigger_volume_a.child_message = new_trigger.artifact_messages[1][1]
        elif num_messages == 3:
            # Create a second trigger
            trigger_volume_b = entity_file.get_entity(
                entity_file.append_entity(copy.deepcopy(template_trigger)), TriggerVolume
            )

            # Activate the second trigger
            trigger_volume_a.child_id = trigger_volume_b.entity_id
            trigger_volume_a.child_message = Message.ACTIVATE

            # Send the second message from the Artifact
            trigger_volume_b.parent_id = new_trigger.artifact_messages[1][0]
            trigger_volume_b.parent_message = new_trigger.artifact_messages[1][1]

            # Send the third message from the Artifact
            trigger_volume_b.child_id = new_trigger.artifact_messages[2][0]
            trigger_volume_b.child_message = new_trigger.artifact_messages[2][1]


class NewObject(NamedTuple):
    area_name: str
    room_name: str
    active_layers: list[int]
    position: tuple[float, float, float]
    scan_id: int
    scan_message_target: int
    scan_message: Message
    node_name: str = "rmMain"
    up_vector_multiplier: int = 1


new_objects = [
    NewObject(
        "Celestial Archives",
        "Helm Room",
        [0, 1, 2],
        (1.450927734375, 4.257568359375, -34.5),
        259,
        8,
        Message.UNLOCK,
        "rmjump",
        -1,
    ),
]


def _add_new_objects(file_manager: FileManager, new_object: NewObject) -> None:
    template_file = file_manager.get_entity_file("Celestial Archives", "Helm Room")
    template_object = copy.deepcopy(template_file.get_entity(9, Object))

    entity_file = file_manager.get_entity_file(new_object.area_name, new_object.room_name)

    # Get the new object
    object_entity = entity_file.get_entity(entity_file.append_entity(template_object), Object)

    # Set the new data fields
    object_entity.node_name = new_object.node_name

    object_entity.position = Vec3(*new_object.position)

    object_entity.up_vector.z *= new_object.up_vector_multiplier

    for layer in new_object.active_layers:
        object_entity.layer_state[layer] = True
