import copy
from typing import NamedTuple

from open_prime_hunters_rando.entities.entity_type import EntityType, Message
from open_prime_hunters_rando.file_manager import FileManager


class NewTrigger(NamedTuple):
    area_name: str
    room_name: str
    active_layers: list[int]
    artifact_id: int
    artifact_messages: list[tuple[int, Message]]
    node_name: str = "rmMain"


new_triggers = [
    NewTrigger(
        "Alinos",
        "High Ground",
        [0, 1, 2, 3],
        24,
        [(17, Message.UNLOCK), (56, Message.UNLOCK_CONNECTORS), (94, Message.TRIGGER)],
    ),
    NewTrigger(
        "Alinos",
        "Elder Passage",
        [0, 1, 2, 3],
        4,
        [(40, Message.TRIGGER), (1, Message.UNLOCK)],
        "rmHallB",
    ),
    NewTrigger(
        "Arcterra",
        "Sic Transit",
        [0, 1, 2],
        35,
        [(6, Message.UNLOCK), (9, Message.UNLOCK)],
    ),
    NewTrigger(
        "Arcterra",
        "Subterranean",
        [0, 1, 2],
        18,
        [(56, Message.ACTIVATE), (58, Message.UNLOCK)],
        "rmSubE",
    ),
]


def _add_triggers(file_manager: FileManager, new_trigger: NewTrigger) -> None:
    template_file = file_manager.get_entity_file("Alinos", "High Ground")
    template_trigger = copy.deepcopy(template_file.get_entity(37))
    template_trigger.trigger_volume_data().active = False

    entity_file = file_manager.get_entity_file(new_trigger.area_name, new_trigger.room_name)
    artifact_entity = entity_file.get_entity(new_trigger.artifact_id)

    # Only add new triggers if the entity is an ItemSpawn
    if artifact_entity.entity_type == EntityType.ARTIFACT:
        return

    # Get the new trigger
    trigger_entity = entity_file.get_entity(entity_file.append_entity(template_trigger))
    trigger_entity.node_name = new_trigger.node_name
    trigger_entity.position = artifact_entity.position

    for layer in new_trigger.active_layers:
        trigger_entity.set_layer_state(layer, True)

    # Update the ItemSpawn to activate the trigger
    new_item_spawn_data = artifact_entity.item_spawn_data()
    new_item_spawn_data.notify_entity_id = trigger_entity.entity_id
    new_item_spawn_data.collected_message = Message.ACTIVATE

    trigger_entity_data = trigger_entity.trigger_volume_data()

    # Send the first message from the Artifact
    trigger_entity_data.parent_id = new_trigger.artifact_messages[0][0]
    trigger_entity_data.parent_message = new_trigger.artifact_messages[0][1]

    num_messages = len(new_trigger.artifact_messages)

    if num_messages == 2:
        # Send the second message from the Artifact
        trigger_entity_data.child_id = new_trigger.artifact_messages[1][0]
        trigger_entity_data.child_message = new_trigger.artifact_messages[1][1]
    elif num_messages == 3:
        # Create a second trigger
        trigger_entity_b = entity_file.get_entity(entity_file.append_entity(copy.deepcopy(template_trigger)))

        # Activate the second trigger
        trigger_entity_data.child_id = trigger_entity_b.entity_id
        trigger_entity_data.child_message = Message.ACTIVATE

        trigger_entity_b.node_name = new_trigger.node_name
        trigger_entity_b_data = trigger_entity_b.trigger_volume_data()

        for layer in new_trigger.active_layers:
            trigger_entity_b.set_layer_state(layer, True)

        # Send the second message from the Artifact
        trigger_entity_b_data.parent_id = new_trigger.artifact_messages[1][0]
        trigger_entity_b_data.parent_message = new_trigger.artifact_messages[1][1]

        # Send the third message from the Artifact
        trigger_entity_b_data.child_id = new_trigger.artifact_messages[2][0]
        trigger_entity_b_data.child_message = new_trigger.artifact_messages[2][1]


class NewObject(NamedTuple):
    area_name: str
    room_name: str
    active_layers: list[int]
    position: tuple[int, int, int]
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


def _add_objects(file_manager: FileManager, new_object: NewObject) -> None:
    template_file = file_manager.get_entity_file("Celestial Archives", "Helm Room")
    template_object = copy.deepcopy(template_file.get_entity(9))

    entity_file = file_manager.get_entity_file(new_object.area_name, new_object.room_name)

    # Get the new object
    object_entity = entity_file.get_entity(entity_file.append_entity(template_object))

    # Set the new data fields
    object_entity.node_name = new_object.node_name

    object_entity.position.x = new_object.position[0]
    object_entity.position.y = new_object.position[1]
    object_entity.position.z = new_object.position[2]

    object_entity.up_vector.z *= new_object.up_vector_multiplier

    for layer in new_object.active_layers:
        object_entity.set_layer_state(layer, True)


def add_new_entities(file_manager: FileManager) -> None:
    # Add new trigger entities
    for new_trigger in new_triggers:
        _add_triggers(file_manager, new_trigger)
    # Add new object entities
    for new_object in new_objects:
        _add_objects(file_manager, new_object)
