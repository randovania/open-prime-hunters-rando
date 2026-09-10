from open_prime_hunters_rando.parsing.common_types.vectors import Vec3
from open_prime_hunters_rando.parsing.formats.entities.entity_file import EntityFile
from open_prime_hunters_rando.parsing.formats.entities.entity_types.light_source import LightSource
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType
from open_prime_hunters_rando.patching.entities import create_rgb_values, get_random_float


def patch_light_sources(entity_file: EntityFile) -> None:
    for entity in entity_file.entities:
        if entity.entity_type != EntityType.LIGHT_SOURCE:
            continue

        light_source = entity_file.get_entity(entity.entity_id, LightSource)

        light_source.light1_color = create_rgb_values()
        light_source.light1_vector = Vec3(get_random_float(), get_random_float(), get_random_float())

        light_source.light2_color = create_rgb_values()
        light_source.light2_vector = Vec3(get_random_float(), get_random_float(), get_random_float())
