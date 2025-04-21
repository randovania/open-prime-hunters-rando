from open_prime_hunters_rando.entities.entity_type import EntityFile


def patch_teleporters(parsed_file: EntityFile, portals: list, room_name: str) -> None:
    for portal in portals:
        entity_id = portal["entity_id"]

        entity = EntityFile.get_entity(parsed_file, entity_id)
        entity.data.load_index = portal["load_index"]
        # entity.data.target_index = portal["target_index"]

        filename: str = portal["entity_filename"]

        if len(filename) < 15:
            raise ValueError(f"{filename} is an invalid length. Expected 15, recieved {len(filename)}!")

        valid_endings = (".", ".b", ".bi")
        if not filename.endswith(valid_endings):
            raise ValueError(f"Invalid entity filename provided for entity {entity_id} in {room_name}!")

        entity.data.entity_filename = filename
