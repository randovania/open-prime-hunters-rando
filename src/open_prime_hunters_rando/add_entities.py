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
    template_trigger = copy.deepcopy(template_file.get_entity(37).data)
    template_trigger.active = False

    entity_file = file_manager.get_entity_file(new_trigger.area_name, new_trigger.room_name)
    artifact_entity = entity_file.get_entity(new_trigger.artifact_id)

    # Only add new triggers if the entity is an ItemSpawn
    if artifact_entity.entity_type == EntityType.ARTIFACT:
        return

    # Get the new trigger
    trigger_entity = entity_file.get_entity(entity_file.append_entity(template_trigger))
    trigger_entity.node_name = new_trigger.node_name
    trigger_entity.data.header.position = artifact_entity.data.header.position

    for layer in new_trigger.active_layers:
        trigger_entity.set_layer_state(layer, True)

    # Update the ItemSpawn to activate the trigger
    artifact_entity.data.notify_entity_id = trigger_entity.entity_id
    artifact_entity.data.collected_message = Message.ACTIVATE

    # Send the first message from the Artifact
    trigger_entity.data.parent_id = new_trigger.artifact_messages[0][0]
    trigger_entity.data.parent_message = new_trigger.artifact_messages[0][1]

    num_messages = len(new_trigger.artifact_messages)

    if num_messages == 2:
        # Send the second message from the Artifact
        trigger_entity.data.child_id = new_trigger.artifact_messages[1][0]
        trigger_entity.data.child_message = new_trigger.artifact_messages[1][1]
    elif num_messages == 3:
        # Create a second trigger
        trigger_entity_b = entity_file.get_entity(entity_file.append_entity(copy.deepcopy(template_trigger)))

        # Activate the second trigger
        trigger_entity.data.child_id = trigger_entity_b.entity_id
        trigger_entity.data.child_message = Message.ACTIVATE

        trigger_entity_b.node_name = new_trigger.node_name

        for layer in new_trigger.active_layers:
            trigger_entity_b.set_layer_state(layer, True)

        # Send the second message from the Artifact
        trigger_entity_b.data.parent_id = new_trigger.artifact_messages[1][0]
        trigger_entity_b.data.parent_message = new_trigger.artifact_messages[1][1]

        # Send the third message from the Artifact
        trigger_entity_b.data.child_id = new_trigger.artifact_messages[2][0]
        trigger_entity_b.data.child_message = new_trigger.artifact_messages[2][1]


def add_new_entities(file_manager: FileManager) -> None:
    for new_trigger in new_triggers:
        _add_triggers(file_manager, new_trigger)
