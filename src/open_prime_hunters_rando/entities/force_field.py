from open_prime_hunters_rando.entities.entity_type import EntityFile


def patch_force_fields(entity_file: EntityFile, force_fields: list) -> None:
    for force_field in force_fields:
        entity_id = force_field["entity_id"]

        entity = EntityFile.get_entity(entity_file, entity_id)
        entity.entity_type = force_field["type"]
