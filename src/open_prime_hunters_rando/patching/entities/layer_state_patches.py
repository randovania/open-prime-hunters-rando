from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemy_spawn import EnemySpawn
from open_prime_hunters_rando.parsing.formats.entities.entity_types.force_field import ForceField
from open_prime_hunters_rando.parsing.formats.entities.entity_types.trigger_volume import TriggerVolume
from open_prime_hunters_rando.parsing.formats.entities.enum import Message


def patch_layer_states(file_manager: FileManager) -> None:
    _disable_escape_triggers(file_manager)
    _remove_disabled_portals(file_manager)
    _disable_boss_force_fields(file_manager)
    _remove_elder_passage_top_lock_and_force_field(file_manager)
    _save_vram_ice_hive(file_manager)
    _patch_specific_layer_states(file_manager)
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
            "Synergy Core": [41, 45, 47],
            "New Arrival Registration": [43, 45],
        },
        "Vesper Defense Outpost": {
            "Weapons Complex": [48, 54, 78],
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


def _disable_boss_force_fields(file_manager: FileManager) -> None:
    boss_force_fields = [
        ("Alinos", "High Ground", 10),
        ("Vesper Defense Outpost", "Weapons Complex", 31),
        ("Arcterra", "Sic Transit", 64),
    ]
    for area_name, room_name, force_field in boss_force_fields:
        entity_file = file_manager.get_entity_file(area_name, room_name)
        entity = entity_file.get_entity(force_field, ForceField)
        # Spire activates the force field until Slench 1 so it has to be disabled outright
        if room_name == "High Ground":
            entity.layer_state[0] = False
            entity.layer_state[3] = False
        else:
            entity.active = False


def _patch_specific_layer_states(file_manager: FileManager) -> None:
    # Patch layer states per room (IDs, Layers, Value)
    patches_per_layer_state: dict[str, dict[str, list[tuple[list[int], list[int], bool]]]] = {
        "Alinos": {
            "Alinos Perch": [
                ([32], [1, 2], True),  # Crash Site Door Unlocked Camera Sequence
            ],
            "Elder Passage": [
                ([11, 18], [1, 2], False),  # Second Pass Doors
            ],
            "High Ground": [
                ([15], [3], True),  # 1st Pass Lower Elder Passage Door
                ([18], [1, 2], False),  # 2nd Pass Elder Passage Moving Platform
                ([56, 72], [1, 2, 3], False),  # Second Pass Bottom Doors
                ([74, 77], [3], True),  # Force Fields
                ([57, 58], [3], True),  # Portals
                ([90, 93], [0, 1, 2], True),  # Artifact Shield Unlocking Camera Sequence
                ([55, 68, 70, 71, 83, 84, 94], [0, 1, 2], True),  # Artifact Platform Activation
            ],
        },
        "Celestial Archives": {
            "Data Shrine 01": [
                ([37], [1, 2], False),  # Second Pass Door
            ],
            "Data Shrine 03": [
                ([47, 48, 49], [2], False),  # FIXME: Random Guardian Spawns can crash if Kanden is active
            ],
            "Incubation Vault 02": [
                ([5, 11], [1, 2], False),  # 2nd pass Psycho Bit and Voldrum spawners
            ],
            "Transfer Lock": [
                ([35, 66], [1, 2], False),  # 2nd pass upper portals (one is active, the other is inactive)
            ],
        },
        "Vesper Defense Outpost": {
            "Weapons Complex": [
                ([5], [1], True),  # Sylux ship on escape layer
                ([27, 33], [2, 3], False),  # FIXME: Sylux ship cannon and camera sequence on second pass to save memory
                ([52, 91], [2], False),  # FIXME: Sylux is always loaded in memory which crashes with random encounters
            ]
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
                (
                    [9, 23, 55, 82, 84, 85, 86, 87, 88],
                    [1, 2],
                    True,
                ),  # Shield Key Scan Points, Trigger, and Camera Sequences
                ([11], [1, 2], False),  # Second Pass Inner Door
                ([24], [1, 2], True),  # First Pass Inner Door
                ([35], [1, 2], True),  # Artifact
                ([61], [1], True),  # Checkpoint
            ],
            "Subterranean": [
                ([44], [1, 2], False),  # Second Pass Elevator
            ],
        },
    }

    for area_name, room_names in patches_per_layer_state.items():
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
            "Council Chamber": [],
            "Crash Site": [],
            "Echo Hall": [],
            "Elder Passage": [],
            "High Ground": [33, 38, 39, 41],  # Slench 1 force fields
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
            "Incubation Vault 03": [],
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
            "Stasis Bunker": [],
            "Weapons Complex": [5, 27, 33],  # Sylux ship and camera sequence
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
                    continue
                # Ensure entities on layer 0 are loaded on layer 1 (during escape) and layer 2 (post escape)
                if entity.layer_state[0]:
                    entity.layer_state[1] = True
                    entity.layer_state[2] = True


def _remove_elder_passage_top_lock_and_force_field(file_manager: FileManager) -> None:
    entity_file = file_manager.get_entity_file("Alinos", "Elder Passage")
    trigger_volume = entity_file.get_entity(25, TriggerVolume)
    trigger_volume.parent_message = Message.NONE

    force_field = entity_file.get_entity(39, ForceField)
    force_field.layer_state[0] = False
    force_field.layer_state[3] = False


def _save_vram_ice_hive(file_manager: FileManager) -> None:
    # Remove some entities to prevent VRAM overflow in large rooms
    entity_file = file_manager.get_entity_file("Arcterra", "Ice Hive")

    # Remove the Carnivorous Plants in the path under the Artifact
    to_remove = [33, 108, 111]
    for entity_id in to_remove:
        carnivorous_plant = entity_file.get_entity(entity_id, EnemySpawn)
        for layer in range(3):
            carnivorous_plant.layer_state[layer] = False
