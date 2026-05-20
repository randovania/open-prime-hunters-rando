import itertools

import pytest

from open_prime_hunters_rando.parsing.common_types.volume import SphereVolumeType, TriggerVolumeFlags
from open_prime_hunters_rando.parsing.formats.entities.entity_file import EntityFile
from open_prime_hunters_rando.parsing.formats.entities.entity_types.door import Door, DoorType
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyType
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.hunter import Hunter, HunterType
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemy_spawn import EnemySpawn
from open_prime_hunters_rando.parsing.formats.entities.entity_types.force_field import ForceField
from open_prime_hunters_rando.parsing.formats.entities.entity_types.trigger_volume import (
    TriggerVolume,
    TriggerVolumeType,
)
from open_prime_hunters_rando.parsing.formats.entities.enum import Message, WeaponType
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
    new_door = Door.create(
        port_name="port_rmMain",
        weapon_type=WeaponType.SHOCK_COIL,
        door_type=DoorType.THIN,
        connector_id=255,
        target_layer_id=12,
        locked=True,
        out_connector_id=10,
        out_loader_id=4,
        entity_file_name="Unit1_Land_Ent",
        room_name="rmMain",
    )

    new_force_field = ForceField.create(
        node_name="rmMain",
        force_field_type=WeaponType.OMEGA_CANNON,
        width=4.0,
        height=2.0,
        active=True,
    )

    new_trigger_volume = TriggerVolume.create(
        node_name="rmMain",
        subtype=TriggerVolumeType.AUTOMATIC,
        volume=SphereVolumeType.create(
            sphere_position=(1.0, 2.0, 3.0),
            sphere_radius=4.0,
        ),
        trigger_flags=TriggerVolumeFlags.INCLUDE_BOTS,
        child_id=0,
        child_message=Message.LOAD_OUBLIETTE,
    )

    new_enemy_spawn = EnemySpawn.create(
        enemy_type=EnemyType.HUNTER,
        enemy_fields=Hunter.create(
            hunter_type=HunterType.SYLUX,
            encounter_type=2,
            hunter_weapon=5,
            hunter_health=10,
            hunter_health_max=20,
            hunter_color=4,
            hunter_chance=50,
        ),
    )

    new_entities = [new_door, new_force_field, new_trigger_volume, new_enemy_spawn]

    parsed = EntityFile.parse(entity_file)

    for new_entity in new_entities:
        parsed.append_entity(new_entity)

        appended_entity = parsed.get_entity(parsed.get_max_entity_id(), type(new_entity))

        assert new_entity == appended_entity

    built = EntityFile.build(parsed)
    assert parsed == EntityFile.parse(built)
