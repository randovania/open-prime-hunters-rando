import itertools

import pytest

from open_prime_hunters_rando.parsing.formats.entities.entity_file import EntityFile, entity_type_to_class
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType
from open_prime_hunters_rando.parsing.level_data import (
    ALINOS,
    ARCTERRA,
    CELESTIAL_ARCHIVES,
    CONNECTORS,
    OUBLIETTE,
    VESPER_DEFENSE_OUTPOST,
)

all_entity_files = [
    level.entity_file
    for level in itertools.chain(
        CONNECTORS.values(),
        ALINOS.values(),
        CELESTIAL_ARCHIVES.values(),
        VESPER_DEFENSE_OUTPOST.values(),
        ARCTERRA.values(),
        OUBLIETTE.values(),
    )
    if level.entity_file is not None
]


@pytest.fixture(scope="module", params=all_entity_files)
def entity_file(rom, request):
    return rom.getFileByName(f"levels/entities/{request.param}.bin")


def test_compare_entity_file(entity_file):
    parsed = EntityFile.parse(entity_file)
    built = EntityFile.build(parsed)

    assert entity_file == built
    assert parsed == EntityFile.parse(built)


def test_create_new_entity(entity_file):
    parsed = EntityFile.parse(entity_file)

    for etype, eclass in entity_type_to_class.items():
        # FIXME: Remove once added
        if etype == EntityType.ENEMY_SPAWN:
            continue
        new_entity = eclass.create()
        parsed.append_entity(new_entity)

        appended_entity = parsed.get_entity(parsed.get_max_entity_id(), type(new_entity))

        assert new_entity == appended_entity

    built = EntityFile.build(parsed)
    assert parsed == EntityFile.parse(built)
