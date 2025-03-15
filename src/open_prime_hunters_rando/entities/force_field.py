from open_prime_hunters_rando.entities.get_entity import get_entity


def patch_force_fields(entity_file: memoryview, force_fields: list) -> None:
    for force_field in force_fields:
        entity_id = force_field["entity_id"]

        data_offset = get_entity(entity_file, entity_id)[0]

        entity_file[data_offset + 40] = force_field["type"]
