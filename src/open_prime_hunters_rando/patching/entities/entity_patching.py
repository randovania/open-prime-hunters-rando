from open_prime_hunters_rando.logger import LOG
from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.parsing.formats.entities.entity_file import EntityFile
from open_prime_hunters_rando.parsing.formats.entities.entity_types.artifact import Artifact
from open_prime_hunters_rando.parsing.formats.entities.enum import Message
from open_prime_hunters_rando.patching.entities import NewTrigger
from open_prime_hunters_rando.patching.entities.add_entities import add_new_entities
from open_prime_hunters_rando.patching.entities.door import patch_doors
from open_prime_hunters_rando.patching.entities.force_field import patch_force_fields
from open_prime_hunters_rando.patching.entities.pickup import patch_pickups
from open_prime_hunters_rando.patching.entities.portal import patch_portals


def patch_entities(file_manager: FileManager, configuration: dict[str, dict]) -> None:
    # List of all artifact triggers with multiple messages
    new_artifact_triggers: list = []

    for area_name, area_config in configuration.items():
        for level_name, level_config in area_config.items():
            for room_name, entity_groups in level_config.items():
                # Load the entity file for the room
                entity_file = file_manager.get_entity_file(area_name, room_name)

                # Create a list of new artifact triggers for artifacts with multiple messages
                artifact_triggers_per_room = _create_artifact_triggers(area_name, room_name, entity_file)

                LOG.info(f"Patching entities in {area_name} - {room_name}")

                # Modify entities
                patch_pickups(entity_file, entity_groups["pickups"], room_name)
                patch_force_fields(entity_file, entity_groups["force_fields"])
                patch_portals(entity_file, entity_groups["portals"], room_name)
                patch_doors(entity_file, entity_groups["doors"], room_name)

                new_artifact_triggers.extend(artifact_triggers_per_room)

    # Add new entities
    LOG.info("Adding new entities")
    add_new_entities(file_manager, new_artifact_triggers)


def _create_artifact_triggers(area_name: str, room_name: str, entity_file: EntityFile) -> list:
    artifact_triggers: list[NewTrigger] = []
    for entity in entity_file.entities:
        if not isinstance(entity, Artifact):
            continue

        message_list: list = []

        artifact_messages: list[tuple[int, Message]] = [
            (entity.message1_target, entity.message1),
            (entity.message2_target, entity.message2),
            (entity.message3_target, entity.message3),
        ]
        for artifact_message in artifact_messages:
            message_target, message = artifact_message
            if message_target == -1 and message == Message.NONE:
                continue
            message_list.append((message_target, message))

        if len(message_list) < 2:
            continue

        artifact_triggers.append(
            NewTrigger(
                area_name=area_name,
                room_name=room_name,
                node_name=entity.node_name,
                active_layers=entity.active_layers,
                entity_id=entity.entity_id,
                artifact_messages=message_list,
            )
        )

    return artifact_triggers
