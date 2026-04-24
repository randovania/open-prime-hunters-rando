from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity


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
    disabled_portal_entities: dict[str, dict[str, list[int]]] = {
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
    # Patch layer states per room (IDs, Entity Type, Layers, Value)
    specific_room_patches: dict[str, dict[str, list[tuple[list[int], list[int], bool]]]] = {
        "Alinos": {
            "Elder Passage": [
                ([11, 18], [1, 2], False),  # Second Pass Doors
            ],
            "High Ground": [
                ([15], [3], True),  # First Pass Bottom Door
                ([56, 72], [1, 2, 3], False),  # Second Pass Bottom Doors
                ([74, 77], [3], True),  # Force Fields
                ([57, 58], [3], True),  # Portals
                ([85, 95], [1], True),  # Hunter Spawns
            ],
        },
        "Celestial Archives": {
            "Data Shrine 01": [
                ([37], [1, 2], False),  # Second Pass Door
            ],
        },
        "Vesper Defense Outpost": {
            # FIXME: This is an ugly workaround to fix the post-boss layer softlock
            "Stasis Bunker": [
                ([4, 5], [1, 2], True),  # Artifacts
                ([21, 79, 90], [1, 2], True),  # Artifact Keys and Item Spawn
            ],
        },
        "Arcterra": {
            "Arcterra Gateway": [
                ([36], [1, 2], True),  # Landing Camera
                ([5, 39], [1], True),  # Teleporter Triggers
            ],
            "Fault Line": [
                ([13], [1, 2], False),  # Knocked Down Pillar
            ],
            "Frost Labyrinth": [
                ([5], [0], False),  # Force Field
            ],
            "Ice Hive": [
                ([65], [1, 2], False),  # Entrance Jump Pad
            ],
            "Sic Transit": [
                ([11], [1, 2], False),  # Second Pass Inner Door
                ([24], [1, 2], True),  # First Pass Inner Door
                ([35], [1, 2], True),  # Artifact
            ],
        },
    }

    for area_name, room_names in specific_room_patches.items():
        for room_name, list_of_entities in room_names.items():
            entity_file = file_manager.get_entity_file(area_name, room_name)
            for entity_ids, layers, state in list_of_entities:
                for entity_id in entity_ids:
                    for layer in layers:
                        entity = entity_file.get_entity(entity_id, Entity)
                        entity.layer_state[layer] = state


def _patch_both_escape_layers(file_manager: FileManager) -> None:
    room_to_patch: dict[str, dict[str, list[int]]] = {
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
            "Incubation Vault 02": [5, 11],  # 2nd pass Voldrum and Psycho Bit Spawners
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
            # FIXME: Figure out how to keep the Sylux encounter on the post-boss layer without softlocking
            "Weapons Complex": [18, 22, 50, 59, 84, 90],  # Sylux Encounter
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
    for area_name, room_names in room_to_patch.items():
        for room_name, excluded_entities in room_names.items():
            entity_file = file_manager.get_entity_file(area_name, room_name)
            for entity in entity_file.entities:
                # Disable entities in this list
                if entity.entity_id in excluded_entities:
                    entity.layer_state[1] = False
                    entity.layer_state[2] = False
                # Workaraound for Data Shrine 03 to prevent softlocking
                if room_name == "Data Shrine 03":
                    entity.layer_state[0] = True
                # Ensure entities on layer 0 are loaded on layer 1 (during escape) and layer 2 (post escape)
                if entity.layer_state[0]:
                    entity.layer_state[1] = True
                    entity.layer_state[2] = True
