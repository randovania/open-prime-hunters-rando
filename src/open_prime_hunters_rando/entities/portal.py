from open_prime_hunters_rando.entities.entity_type import EntityFile
from open_prime_hunters_rando.level_data import ALL_PORTAL_FILENAMES


def patch_portals(entity_file: EntityFile, portals: list, room_name: str) -> None:
    for portal in portals:
        entity_id = portal["entity_id"]
        filename: str = portal["entity_filename"]

        entity = entity_file.get_entity(entity_id)

        # target_index is the load_index of the desination portal
        entity.data.target_index = portal["target_index"]

        if filename not in ALL_PORTAL_FILENAMES:
            raise ValueError(f"Invalid entity filename for portal entity {entity_id} in {room_name}: {filename}")
        filename = f"{filename}.bin"
        filename = filename[:15]

        entity.data.entity_filename = filename
