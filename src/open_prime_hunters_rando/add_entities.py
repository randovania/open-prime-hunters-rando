import copy

from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.entities.entity_type import Entity, EntityFile, EntityType, Message
from open_prime_hunters_rando.level_data import get_entity_file


def add_new_entities(rom: NintendoDSRom) -> None:
    file_name, parsed_file = get_entity_file(rom, "Alinos", "High Ground")
    template_entity = EntityFile.get_entity(parsed_file, 37).data
    template_entity.active = False

    _high_ground(rom, template_entity)
    _elder_passage(rom, template_entity)
    _sic_transit(rom, template_entity)
    _subterranean(rom, template_entity)


def _set_new_entity_id(parsed_file: EntityFile, template_entity: Entity) -> int:
    max_entity_id = EntityFile.get_max_entity_id(parsed_file)
    template_entity.header.entity_id = max_entity_id
    parsed_file.entities.append(Entity.create(template_entity))
    return max_entity_id


def _high_ground(rom: NintendoDSRom, template_entity: Entity) -> None:
    file_name, parsed_file = get_entity_file(rom, "Alinos", "High Ground")
    artifact_entity = EntityFile.get_entity(parsed_file, 24)

    # Only add new triggers if the entity is an ItemSpawn
    if artifact_entity.entity_type == EntityType.ARTIFACT:
        return

    # Get the first new trigger
    new_trigger_a = EntityFile.get_entity(parsed_file, _set_new_entity_id(parsed_file, template_entity))

    # Update the ItemSpawn to activate the first trigger
    artifact_entity.data.notify_entity_id = new_trigger_a.entity_id
    artifact_entity.data.collected_message = Message.ACTIVATE

    # Send the first message from the Artifact
    new_trigger_a.data.parent_id = 17
    new_trigger_a.data.parent_message = Message.UNLOCK

    # Get the second new trigger
    new_trigger_b = EntityFile.get_entity(parsed_file, _set_new_entity_id(parsed_file, copy.deepcopy(template_entity)))

    # Activate the second trigger
    new_trigger_a.data.child_id = new_trigger_b.entity_id
    new_trigger_a.data.child_message = Message.ACTIVATE

    for trigger in [new_trigger_a, new_trigger_b]:
        trigger.node_name = "rmMain"
        trigger.data.header.position = artifact_entity.data.header.position

        for layer_state in range(4, 16):
            trigger.set_layer_state(layer_state, False)

    # Send the second message from the Artifact
    new_trigger_b.data.parent_id = 56
    new_trigger_b.data.parent_message = Message.UNLOCK_CONNECTORS
    # Send the third message from the Artifact
    new_trigger_b.data.child_id = 94
    new_trigger_b.data.child_message = Message.TRIGGER

    rom.setFileByName(file_name, EntityFile.build(parsed_file))


def _elder_passage(rom: NintendoDSRom, template_entity: Entity) -> None:
    file_name, parsed_file = get_entity_file(rom, "Alinos", "Elder Passage")
    artifact_entity = EntityFile.get_entity(parsed_file, 4)

    # Only add new triggers if the entity is an ItemSpawn
    if artifact_entity.entity_type == EntityType.ARTIFACT:
        return

    # Get the new trigger
    new_trigger = EntityFile.get_entity(parsed_file, _set_new_entity_id(parsed_file, template_entity))
    new_trigger.node_name = "rmHallB"
    new_trigger.data.header.position = artifact_entity.data.header.position

    for layer_state in range(4, 16):
        new_trigger.set_layer_state(layer_state, False)

    # Update the ItemSpawn to activate the trigger
    artifact_entity.data.notify_entity_id = new_trigger.entity_id
    artifact_entity.data.collected_message = Message.ACTIVATE

    # Send the first message from the Artifact
    new_trigger.data.parent_id = 40
    new_trigger.data.parent_message = Message.TRIGGER
    # Send the second message from the Artifact
    new_trigger.data.child_id = 1
    new_trigger.data.child_message = Message.UNLOCK

    rom.setFileByName(file_name, EntityFile.build(parsed_file))


def _sic_transit(rom: NintendoDSRom, template_entity: Entity) -> None:
    file_name, parsed_file = get_entity_file(rom, "Arcterra", "Sic Transit")
    artifact_entity = EntityFile.get_entity(parsed_file, 35)

    # Only add new triggers if the entity is an ItemSpawn
    if artifact_entity.entity_type == EntityType.ARTIFACT:
        return

    # Get the new trigger
    new_trigger = EntityFile.get_entity(parsed_file, _set_new_entity_id(parsed_file, template_entity))
    new_trigger.node_name = "rmMain"
    new_trigger.data.header.position = artifact_entity.data.header.position

    for layer_state in range(3, 16):
        new_trigger.set_layer_state(layer_state, False)

    # Update the ItemSpawn to activate the trigger
    artifact_entity.data.notify_entity_id = new_trigger.entity_id
    artifact_entity.data.collected_message = Message.ACTIVATE

    # Send the first message from the Artifact
    new_trigger.data.parent_id = 6
    new_trigger.data.parent_message = Message.UNLOCK
    # Send the second message from the Artifact
    new_trigger.data.child_id = 9
    new_trigger.data.child_message = Message.UNLOCK

    rom.setFileByName(file_name, EntityFile.build(parsed_file))


def _subterranean(rom: NintendoDSRom, template_entity: Entity) -> None:
    file_name, parsed_file = get_entity_file(rom, "Arcterra", "Subterranean")
    artifact_entity = EntityFile.get_entity(parsed_file, 18)

    # Only add new triggers if the entity is an ItemSpawn
    if artifact_entity.entity_type == EntityType.ARTIFACT:
        return

    # Get the new trigger
    new_trigger = EntityFile.get_entity(parsed_file, _set_new_entity_id(parsed_file, template_entity))
    new_trigger.node_name = "rmSubE"
    new_trigger.data.header.position = artifact_entity.data.header.position

    for layer_state in range(3, 16):
        new_trigger.set_layer_state(layer_state, False)

    # Update the ItemSpawn to activate the trigger
    artifact_entity.data.notify_entity_id = new_trigger.entity_id
    artifact_entity.data.collected_message = Message.ACTIVATE

    # Send the first message from the Artifact
    new_trigger.data.parent_id = 56
    new_trigger.data.parent_message = Message.ACTIVATE
    # Send the second message from the Artifact
    new_trigger.data.child_id = 58
    new_trigger.data.child_message = Message.UNLOCK

    rom.setFileByName(file_name, EntityFile.build(parsed_file))
