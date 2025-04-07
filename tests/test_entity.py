import pytest
from open_prime_hunters_rando.entities.entity_type import Entity, EntityFile, EntityType
from construct import Container


@pytest.fixture(scope="session")
def entity_file(rom):
    return rom.getFileByName("levels/entities/unit2_RM2_Ent.bin")


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
