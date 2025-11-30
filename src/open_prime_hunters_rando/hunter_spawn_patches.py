import random

from open_prime_hunters_rando.entities.entity_type import EnemyType, EntityFile, EntityType, Field9, Hunter
from open_prime_hunters_rando.file_manager import FileManager
from open_prime_hunters_rando.logger import LOG

ROOMS_WITH_HUNTERS: dict[str, dict[str, dict[int, int]]] = {
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

    LOG.info("Modifying hunter spawns")
    random.seed(configuration["configuration_id"])

    if shuffle_hunter_colors:
        hunter_colors = list(range(6))
        hunters_to_color = {
            Hunter.SAMUS: random.choice(hunter_colors),
            Hunter.KANDEN: random.choice(hunter_colors),
            Hunter.TRACE: random.choice(hunter_colors),
            Hunter.SYLUX: random.choice(hunter_colors),
            Hunter.NOXUS: random.choice(hunter_colors),
            Hunter.SPIRE: random.choice(hunter_colors),
            Hunter.WEAVEL: random.choice(hunter_colors),
            Hunter.GUARDIAN: random.choice(hunter_colors),
            Hunter.RANDOM: random.choice(hunter_colors),
        }

    for area_name, room_names in ROOMS_WITH_HUNTERS.items():
        for room_name, encounter_type_entities in room_names.items():
            entity_file = file_manager.get_entity_file(area_name, room_name)
            for entity in entity_file.entities:
                if entity.entity_type != EntityType.ENEMY_SPAWN:
                    continue
                if entity.enemy_spawn_data().enemy_type != EnemyType.HUNTER:
                    continue

                if shuffle_hunter_ids:
                    # Have "Spire" spawns in High Ground and Elder Passage match
                    if room_name == "High Ground" and entity.entity_id in [21, 60]:
                        elder_passage = file_manager.get_entity_file("Alinos", "Elder Passage")
                        spire_data = elder_passage.get_entity(9).enemy_spawn_data().get_enemy_spawn_field_9()
                        new_hunter_id = spire_data.hunter_id
                    # Spawning a Guardian causes a crash in Data Shrine 03 "Kanden" spawn
                    elif room_name == "Data Shrine 02" and entity.entity_id == 12:
                        new_hunter_id = Hunter(random.choice(list(range(1, 7))))
                    # Have "Kanden" spawns in Data Shrine 02 and Data Shrine 03 match
                    elif room_name == "Data Shrine 03" and entity.entity_id == 3:
                        data_shrine_02 = file_manager.get_entity_file("Celestial Archives", "Data Shrine 02")
                        kanden_data = data_shrine_02.get_entity(12).enemy_spawn_data().get_enemy_spawn_field_9()
                        new_hunter_id = kanden_data.hunter_id
                    # TODO: Figure out why Weapons Complex crashes when shuffling the hunters
                    elif room_name == "Weapons Complex":
                        continue
                    else:
                        # If enabled, generate a new hunter id (1-7) and modify the entity
                        new_hunter_id = Hunter(random.choice(list(range(1, 8))))

                    hunter_data = entity.enemy_spawn_data().get_enemy_spawn_field_9()
                    # Only modify the hunter fields if the hunter id is different
                    if hunter_data.hunter_id != new_hunter_id:
                        _patch_hunter_ids(hunter_data, new_hunter_id)
                        _patch_encounter_types(entity_file, encounter_type_entities)

                if shuffle_hunter_colors:
                    # If enabled, change the hunter spawns to use a random color by hunter type (0-5)
                    fields = entity.enemy_spawn_data().get_enemy_spawn_field_9()
                    fields.hunter_color = hunters_to_color.get(fields.hunter_id, 0)


def _patch_hunter_ids(hunter_data: Field9, new_hunter_id: Hunter) -> None:
    # Set the new hunter id
    hunter_data.hunter_id = new_hunter_id
    if new_hunter_id == Hunter.GUARDIAN:
        # Guardians can use weapon except Omega Cannon
        hunter_data.hunter_weapon = random.choice(list(range(8)))
    else:
        # Hunters by default use a weapon value of 255
        hunter_data.hunter_weapon = 255


def _patch_encounter_types(entity_file: EntityFile, encounter_type_entities: dict[int, int]) -> None:
    # Handle certain hunter spawns not functioning properly
    for entity_id, encounter_type in encounter_type_entities.items():
        entity = entity_file.get_entity(entity_id).enemy_spawn_data().get_enemy_spawn_field_9()
        entity.encounter_type = encounter_type
