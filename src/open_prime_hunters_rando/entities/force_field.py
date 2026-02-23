from open_prime_hunters_rando.entities.entity_file import EntityFile
from open_prime_hunters_rando.entities.entity_types.force_field import ForceField
from open_prime_hunters_rando.entities.enum import PaletteId


def patch_force_fields(entity_file: EntityFile, force_fields: list) -> None:
    for force_field in force_fields:
        entity_id = force_field["entity_id"]

        entity = entity_file.get_entity(entity_id, ForceField)
        entity.type = PaletteId(force_field["type"])
