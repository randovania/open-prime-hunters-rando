from construct import Construct

from open_prime_hunters_rando.constants import get_entity


def patch_force_fields(entity_file: Construct, force_fields: list) -> None:
    for force_field in force_fields:
        entity_id = force_field["entity_id"]
        entity_idx = get_entity(entity_file, entity_id)

        entity = entity_file.entities[entity_idx]
        entity.data.type = force_field["type"]
