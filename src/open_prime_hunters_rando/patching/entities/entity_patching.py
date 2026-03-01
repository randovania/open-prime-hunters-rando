from open_prime_hunters_rando.logger import LOG
from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.patching.entities.door import patch_doors
from open_prime_hunters_rando.patching.entities.force_field import patch_force_fields
from open_prime_hunters_rando.patching.entities.pickup import patch_pickups
from open_prime_hunters_rando.patching.entities.portal import patch_portals


def patch_entities(file_manager: FileManager, configuration: dict[str, dict]) -> None:
    for area_name, area_config in configuration.items():
        for level_name, level_config in area_config.items():
            for room_name, entity_groups in level_config.items():
                # Load the entity file for the room
                entity_file = file_manager.get_entity_file(area_name, room_name)

                LOG.info(f"Patching entities in {area_name} - {room_name}")

                # Modify entities
                patch_pickups(entity_file, entity_groups["pickups"])
                patch_force_fields(entity_file, entity_groups["force_fields"])
                patch_portals(entity_file, entity_groups["portals"], room_name)
                patch_doors(entity_file, entity_groups["doors"], room_name)
