import itertools

import pytest

from open_prime_hunters_rando.parsing.formats.entities.entity_file import EntityFile
from open_prime_hunters_rando.parsing.formats.entities.entity_types.door import Door, DoorType
from open_prime_hunters_rando.parsing.formats.entities.enum import PaletteId
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
    new_entity = Door.create(
        port_name="port_rmMain",
        palette_id=PaletteId.SHOCK_COIL,
        door_type=DoorType.THIN,
        connector_id=255,
        target_layer_id=12,
        locked=True,
        out_connector_id=10,
        out_loader_id=4,
        entity_file_name="Unit1_Land_Ent",
        room_name="rmMain",
    )

    parsed = EntityFile.parse(entity_file)
    max_entity_id = parsed.get_max_entity_id()
    parsed.replace_entity(max_entity_id, new_entity)

    replaced_entity = parsed.get_entity(max_entity_id, Door)

    assert new_entity == replaced_entity

    built = EntityFile.build(parsed)
    assert parsed == EntityFile.parse(built)
