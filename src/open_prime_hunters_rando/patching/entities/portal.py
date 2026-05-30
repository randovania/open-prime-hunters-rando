from open_prime_hunters_rando.parsing.formats.entities.entity_file import EntityFile
from open_prime_hunters_rando.parsing.formats.entities.entity_types.teleporter import Teleporter
from open_prime_hunters_rando.parsing.level_data import ALL_PORTAL_FILE_NAMES


def patch_portals(entity_file: EntityFile, portals: list, room_name: str) -> None:
    for portal in portals:
        entity_id = portal["entity_id"]
        file_name: str = portal["entity_file_name"]

        entity = entity_file.get_entity(entity_id, Teleporter)

        # target_index is the load_index of the desination portal
        entity.target_index = portal["target_index"]

        if file_name not in ALL_PORTAL_FILE_NAMES:
            raise ValueError(f"Invalid entity file_name for portal entity {entity_id} in {room_name}: {file_name}")
        file_name = f"{file_name}.bin"
        file_name = file_name[:15]

        entity.entity_file_name = file_name
