from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_types.force_field import ForceField
from open_prime_hunters_rando.parsing.formats.entities.entity_types.item_spawn import ItemSpawn


def patch_escape_sequences(file_manager: FileManager) -> None:
    _disable_escape_triggers(file_manager)
    _remove_disabled_portals(file_manager)
    _patch_specific_rooms(file_manager)
    _patch_both_escape_layers(file_manager)


def _disable_escape_triggers(file_manager: FileManager) -> None:
    areas = ["Alinos", "Celestial Archives", "Vesper Defense Outpost", "Arcterra"]
    stronghold_voids = ["A", "B"]
    escape_triggers = []
    for area in areas:
        for stronghold_void in stronghold_voids:
            entity_file = file_manager.get_entity_file(area, f"Stronghold Void {stronghold_void}")
            # The Show_Prompt trigger has a different id in three rooms
            if area == "Celestial Archives" and stronghold_void == "A":
                escape_triggers = [5, 8]
            elif area == "Arcterra":
                escape_triggers = [4, 5]
            else:
                escape_triggers = [5, 16]

            for escape_trigger in escape_triggers:
                entity = entity_file.get_entity(escape_trigger, Entity)
                entity.layer_state[1] = False


def _remove_disabled_portals(file_manager: FileManager) -> None:
    disabled_portal_entities = {
        "Alinos": {
            "Elder Passage": [21, 24],
            "Council Chamber": [54, 57],
        },
        "Celestial Archives": {
            "Synergy Core": [47, 45],
            "New Arrival Registration": [43, 45],
        },
        "Vesper Defense Outpost": {
            "Weapons Complex": [78, 54],
            "Ascension": [38, 6],
        },
        "Arcterra": {
            "Ice Hive": [174, 207],
            "Fault Line": [76, 73],
        },
    }
    for area_name, room_names in disabled_portal_entities.items():
        for room_name, portal_entities in room_names.items():
            entity_file = file_manager.get_entity_file(area_name, room_name)
            for portal_entity in portal_entities:
                entity = entity_file.get_entity(portal_entity, Entity)
                entity.layer_state[1] = False


def _patch_specific_rooms(file_manager: FileManager) -> None:
    # High Ground
    entity_file = file_manager.get_entity_file("Alinos", "High Ground")

    first_pass_bottom_door = entity_file.get_entity(15, Entity)
    first_pass_bottom_door.layer_state[3] = True

    second_pass_bottom_doors = [56, 72]
    for door in second_pass_bottom_doors:
        entity = entity_file.get_entity(door, Entity)
        for layer in range(1, 4):
            entity.layer_state[layer] = False

    force_fields = [74, 77]
    for force_field_id in force_fields:
        entity = entity_file.get_entity(force_field_id, Entity)
        entity.layer_state[3] = True

    portals = [57, 58]
    for portal in portals:
        entity = entity_file.get_entity(portal, Entity)
        entity.layer_state[3] = True

    hunters = [85, 95]
    for hunter in hunters:
        entity = entity_file.get_entity(hunter, Entity)
        entity.layer_state[1] = True

    # Elder Passage
    entity_file = file_manager.get_entity_file("Alinos", "Elder Passage")

    second_pass_doors = [11, 18]
    for door in second_pass_doors:
        entity = entity_file.get_entity(door, Entity)
        for layer in range(1, 3):
            entity.layer_state[layer] = False

    # Data Shrine 01
    entity_file = file_manager.get_entity_file("Celestial Archives", "Data Shrine 01")

    second_pass_door = entity_file.get_entity(37, Entity)
    second_pass_door.layer_state[1] = False
    second_pass_door.layer_state[2] = False

    # Weapons Complex
    entity_file = file_manager.get_entity_file("Vesper Defense Outpost", "Weapons Complex")

    # FIXME: Figure out how to keep the Sylux encounter on the post-boss layer without softlocking
    artifact_key = entity_file.get_entity(38, ItemSpawn)
    artifact_key.enabled = True

    wc_force_fields = [34, 36]
    for id in wc_force_fields:
        wc_force_field = entity_file.get_entity(id, ForceField)
        wc_force_field.active = False

    # Stasis Bunker
    entity_file = file_manager.get_entity_file("Vesper Defense Outpost", "Stasis Bunker")

    item_spawns = [4, 5, 21, 79, 90]
    for item_spawn in item_spawns:
        # FIXME: This is an ugly workaround to fix the post-boss layer softlock
        entity = entity_file.get_entity(item_spawn, Entity)
        entity.layer_state[1] = True
        entity.layer_state[2] = True

    # Frost Labyrinth
    entity_file = file_manager.get_entity_file("Arcterra", "Frost Labyrinth")

    force_field = entity_file.get_entity(5, Entity)
    force_field.layer_state[0] = False

    # Arcterra Gateway
    entity_file = file_manager.get_entity_file("Arcterra", "Arcterra Gateway")

    # Landing camera
    camera_sequence = entity_file.get_entity(36, Entity)
    camera_sequence.layer_state[1] = True
    camera_sequence.layer_state[2] = True

    # Teleporter triggers
    trigger_volumes = [5, 39]
    for trigger_volume in trigger_volumes:
        entity = entity_file.get_entity(trigger_volume, Entity)
        entity.layer_state[1] = True

    # Ice Hive
    entity_file = file_manager.get_entity_file("Arcterra", "Ice Hive")

    entrance_jump_pad = entity_file.get_entity(65, Entity)
    entrance_jump_pad.layer_state[1] = False
    entrance_jump_pad.layer_state[2] = False

    # Sic Transit
    entity_file = file_manager.get_entity_file("Arcterra", "Sic Transit")

    first_pass_inner_door = entity_file.get_entity(24, Entity)
    first_pass_inner_door.layer_state[1] = True
    first_pass_inner_door.layer_state[2] = True

    second_pass_inner_door = entity_file.get_entity(11, Entity)
    second_pass_inner_door.layer_state[1] = False
    second_pass_inner_door.layer_state[2] = False

    artifact = entity_file.get_entity(35, Entity)
    artifact.layer_state[1] = True
    artifact.layer_state[2] = True

    # Fault Line
    entity_file = file_manager.get_entity_file("Arcterra", "Fault Line")

    knocked_down_pillar = entity_file.get_entity(13, Entity)
    knocked_down_pillar.layer_state[1] = False
    knocked_down_pillar.layer_state[2] = False


def _patch_both_escape_layers(file_manager: FileManager) -> None:
    ROOMS_TO_PATCH: dict[str, dict[str, list[int]]] = {
        "Alinos": {
            "Alinos Gateway": [],
            "Council Chamber": [35, 37],  # First pass Guardians
            "Crash Site": [],
            "Echo Hall": [],
            "Elder Passage": [39],  # Spire top force field
            "High Ground": [10, 33, 38, 39, 41],  # Slench 1 force fields
            "Piston Cave": [],
            "Processor Core": [],
        },
        "Celestial Archives": {
            "Celestial Gateway": [],
            "Data Shrine 01": [],
            "Data Shrine 03": [],
            "Docking Bay": [],
            "Incubation Vault 01": [],
            "Incubation Vault 02": [],
            "New Arrival Registration": [],
            "Synergy Core": [],
            "Tetra Vista": [],
            "Transfer Lock": [],
        },
        "Vesper Defense Outpost": {
            "Ascension": [],
            "Compression Chamber": [],
            "Cortex CPU": [],
            "Fuel Stack": [],
            "VDO Gateway": [],
            "Weapons Complex": [18, 22, 59, 84, 90],  # Sylux Encounter
        },
        "Arcterra": {
            "Drip Moat": [],
            "Fault Line": [],
            "Frost Labyrinth": [],
            "Ice Hive": [],
            "Sanctorus": [],
            "Subterranean": [],
        },
    }
    for area_name, room_names in ROOMS_TO_PATCH.items():
        for room_name, skipped_entities in room_names.items():
            entity_file = file_manager.get_entity_file(area_name, room_name)
            for entity in entity_file.entities:
                # Skip modifying any entities in this list
                if entity.entity_id in skipped_entities:
                    continue
                # Ensure entities on layer 0 are loaded on layer 1 (during escape) and layer 2 (post escape)
                elif entity.layer_state[0]:
                    entity.layer_state[1] = True
                    entity.layer_state[2] = True
