import itertools
from open_prime_hunters_rando.level_data import ALINOS, ARCTERRA, CELESTIAL_ARCHIVES, CONNECTORS, OUBLIETTE, VESPER_DEFENSE_OUTPOST
import pytest
from open_prime_hunters_rando.entities.entity_type import Entity, EntityFile, EntityType
from construct import Container


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


def test_add_entity(entity_file):
    parsed = EntityFile.parse(entity_file)
    parsed.entities.append(Entity.create(Container({
        "header": Container({
            "entity_type": EntityType.OCTOLITH_FLAG,
            "entity_id": 0,
            "position": {"x": 0.0, "y": 0.0, "z": 0.0},
            "up_vector": {"x": 0.0, "y": 0.0, "z": 0.0},
            "facing_vector": {"x": 0.0, "y": 0.0, "z": 0.0},
        }),
        "team_id": 0,
    })))

    built = EntityFile.build(parsed)
    assert parsed == EntityFile.parse(built)
