import random

from construct import Container

from open_prime_hunters_rando.entities.entity_type import EnemyType, EntityFile, EntityType, Hunter
from open_prime_hunters_rando.file_manager import FileManager

_ROOMS_WITH_HUNTERS = {
    "Alinos": {
        "Alinos Perch": {},
        "Combat Hall": {},
        "Council Chamber": {},
        "Echo Hall": {},
        "Elder Passage": {},
        "High Ground": {21: 4},
        "Processor Core": {},
    },
    "Celestial Archives": {
        "Data Shrine 01": {},
        "Data Shrine 02": {},
        "Data Shrine 03": {3: 0},
        "Docking Bay": {},
        "Helm Room": {},
        "Incubation Vault 01": {},
        "Incubation Vault 02": {},
        "Incubation Vault 03": {},
        "Transfer Lock": {},
    },
    "Vesper Defense Outpost": {
        "Compression Chamber": {},
        "Stasis Bunker": {},
        "Weapons Complex": {},
    },
    "Arcterra": {
        "Arcterra Gateway": {},
        "Fault Line": {},
        "Sanctorus": {},
        "Sic Transit": {},
        "Subterranean": {},
    },
}


def patch_hunters(file_manager: FileManager, configuration: dict) -> None:
    shuffle_hunter_colors = configuration["game_patches"]["shuffle_hunter_colors"]
    shuffle_hunter_ids = configuration["game_patches"]["shuffle_hunter_ids"]

    if not shuffle_hunter_colors and not shuffle_hunter_ids:
        return

    random.seed(configuration["configuration_id"])

    for area_name, room_names in _ROOMS_WITH_HUNTERS.items():
        for room_name, encounter_type_entities in room_names.items():
            entity_file = file_manager.get_entity_file(area_name, room_name)
            for entity in entity_file.entities:
                if entity.entity_type != EntityType.ENEMY_SPAWN:
                    continue
                if entity.data.enemy_type != EnemyType.HUNTER:
                    continue

                if shuffle_hunter_colors:
                    # If enabled, change the hunter spawns to use a random color (0-6)
                    entity.data.fields.hunter_color = random.choice(list(range(6)))

                if shuffle_hunter_ids:
                    # If enabled, generate a new hunter id (0-8) and modify the entity
                    new_hunter_id = Hunter(random.choice(list(range(8))))
                    hunter_data = entity.data.fields
                    # Only modify the hunter fields if the hunter id is different
                    if hunter_data.hunter_id != new_hunter_id:
                        _patch_hunter_ids(hunter_data, new_hunter_id)
                        _patch_encounter_types(entity_file, encounter_type_entities)


def _patch_hunter_ids(hunter_data: Container, new_hunter_id: Hunter) -> None:
    # Set the new hunter id
    hunter_data.hunter_id = new_hunter_id
    if new_hunter_id != Hunter.SPIRE:
        if new_hunter_id == Hunter.GUARDIAN:
            # Guardians can use weapon except Omega Cannon
            hunter_data.hunter_weapon = random.choice(list(range(8)))
        else:
            # Hunters by default use a weapon value of 255
            hunter_data.hunter_weapon = 255
    else:
        # Spire is the only non-Guardian hunter that has the weapon preset (might not be important)
        hunter_data.hunter_weapon = 6


def _patch_encounter_types(entity_file: EntityFile, encounter_type_entities: dict[int, int]) -> None:
    # Handle certain hunter spawns not functioning properly
    for entity_id, encounter_type in encounter_type_entities.items():
        entity = entity_file.get_entity(entity_id)
        entity.data.fields.encounter_type = encounter_type
