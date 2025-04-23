from open_prime_hunters_rando.entities.entity_type import EntityFile


def patch_portals(entity_file: EntityFile, portals: list, room_name: str) -> None:
    for portal in portals:
        entity_id = portal["entity_id"]
        filename: str = portal["entity_filename"]

        entity = entity_file.get_entity(entity_id)

        # target_index is the load_index of the desination portal
        entity.data.target_index = portal["target_index"]

        # filenames must have a length of 15
        if len(filename) != 15:
            raise ValueError(f"{filename} is an invalid length. Expected 15, recieved {len(filename)}!")

        # filenames must end with certain characters
        valid_endings = (".", ".b", ".bi")
        if not filename.endswith(valid_endings):
            raise ValueError(f"Invalid entity filename provided for entity {entity_id} in {room_name}!")

        entity.data.entity_filename = filename
