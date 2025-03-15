from open_prime_hunters_rando.entities.entity_data import LevelData


def patch_force_fields(entity_file: memoryview, level_data: LevelData, force_fields: list) -> None:
    for force_field in force_fields:
        for entity_data in level_data.entities:
            if force_field["entity_id"] == entity_data.entity_id:
                entity_file[entity_data.offset + 40] = force_field["type"]
