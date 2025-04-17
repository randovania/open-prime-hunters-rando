from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.entities.entity_type import EntityFile
from open_prime_hunters_rando.level_data import get_entity_file


def patch_escape_sequences(rom: NintendoDSRom) -> None:
    _disable_escape_triggers(rom)
    _remove_disabled_portals(rom)
    _patch_specific_rooms(rom)
    _patch_both_escape_layers(rom)


def _disable_escape_triggers(rom: NintendoDSRom) -> None:
    areas = ["Alinos", "Celestial Archives", "Vesper Defense Outpost", "Arcterra"]
    stronghold_voids = ["A", "B"]
    escape_triggers = []
    for area in areas:
        for stronghold_void in stronghold_voids:
            file_name, parsed_file = get_entity_file(rom, area, f"Stronghold Void {stronghold_void}")
            # The Show_Prompt trigger has a different id in three rooms
            if area == "Celestial Archives" and stronghold_void == "A":
                escape_triggers = [5, 8]
            elif area == "Arcterra":
                escape_triggers = [4, 5]
            else:
                escape_triggers = [5, 16]

            for escape_trigger in escape_triggers:
                entity = EntityFile.get_entity(parsed_file, escape_trigger)
                entity.set_layer_state(1, False)

            rom.setFileByName(file_name, EntityFile.build(parsed_file))


def _remove_disabled_portals(rom: NintendoDSRom) -> None:
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
            file_name, parsed_file = get_entity_file(rom, area_name, room_name)
            for portal_entity in portal_entities:
                entity = EntityFile.get_entity(parsed_file, portal_entity)
                entity.set_layer_state(1, False)

            rom.setFileByName(file_name, EntityFile.build(parsed_file))


def _patch_specific_rooms(rom: NintendoDSRom) -> None:
    # High Ground
    file_name, parsed_file = get_entity_file(rom, "Alinos", "High Ground")

    first_pass_bottom_door = EntityFile.get_entity(parsed_file, 15)
    first_pass_bottom_door.set_layer_state(3, True)

    second_pass_bottom_doors = [56, 72]
    for door in second_pass_bottom_doors:
        entity = EntityFile.get_entity(parsed_file, door)
        for layer in range(1, 4):
            entity.set_layer_state(layer, False)

    force_fields = [74, 77]
    for force_field in force_fields:
        entity = EntityFile.get_entity(parsed_file, force_field)
        entity.set_layer_state(3, True)

    portals = [57, 58]
    for portal in portals:
        entity = EntityFile.get_entity(parsed_file, portal)
        entity.set_layer_state(3, True)

    rom.setFileByName(file_name, EntityFile.build(parsed_file))

    # Elder Passage
    file_name, parsed_file = get_entity_file(rom, "Alinos", "Elder Passage")

    second_pass_doors = [11, 18]
    for door in second_pass_doors:
        entity = EntityFile.get_entity(parsed_file, door)
        for layer in range(1, 3):
            entity.set_layer_state(layer, False)

    rom.setFileByName(file_name, EntityFile.build(parsed_file))

    # Alinos Perch
    file_name, parsed_file = get_entity_file(rom, "Alinos", "Alinos Perch")

    second_pass_door = EntityFile.get_entity(parsed_file, 5)
    second_pass_door.set_layer_state(1, False)
    second_pass_door.set_layer_state(2, False)

    rom.setFileByName(file_name, EntityFile.build(parsed_file))

    # Data Shrine 01
    file_name, parsed_file = get_entity_file(rom, "Celestial Archives", "Data Shrine 01")

    second_pass_door = EntityFile.get_entity(parsed_file, 37)
    second_pass_door.set_layer_state(1, False)
    second_pass_door.set_layer_state(2, False)

    rom.setFileByName(file_name, EntityFile.build(parsed_file))

    # Frost Labyrinth
    file_name, parsed_file = get_entity_file(rom, "Arcterra", "Frost Labyrinth")

    force_field = EntityFile.get_entity(parsed_file, 5)
    second_pass_door.set_layer_state(0, False)

    rom.setFileByName(file_name, EntityFile.build(parsed_file))

    # Arcterra Gateway
    file_name, parsed_file = get_entity_file(rom, "Arcterra", "Arcterra Gateway")

    # Landing camera
    camera_sequence = EntityFile.get_entity(parsed_file, 36)
    camera_sequence.set_layer_state(1, True)
    camera_sequence.set_layer_state(2, True)

    # Teleporter triggers
    trigger_volumes = [5, 39]
    for trigger_volume in trigger_volumes:
        entity = EntityFile.get_entity(parsed_file, trigger_volume)
        entity.set_layer_state(1, True)

    rom.setFileByName(file_name, EntityFile.build(parsed_file))

    # Ice Hive
    file_name, parsed_file = get_entity_file(rom, "Arcterra", "Ice Hive")

    entrance_jump_pad = EntityFile.get_entity(parsed_file, 65)
    entrance_jump_pad.set_layer_state(1, False)
    entrance_jump_pad.set_layer_state(2, False)

    rom.setFileByName(file_name, EntityFile.build(parsed_file))

    # Sic Transit
    file_name, parsed_file = get_entity_file(rom, "Arcterra", "Sic Transit")

    first_pass_inner_door = EntityFile.get_entity(parsed_file, 24)
    first_pass_inner_door.set_layer_state(1, True)
    first_pass_inner_door.set_layer_state(2, True)

    second_pass_inner_door = EntityFile.get_entity(parsed_file, 11)
    second_pass_inner_door.set_layer_state(1, False)
    second_pass_inner_door.set_layer_state(2, False)

    artifact = EntityFile.get_entity(parsed_file, 35)
    artifact.set_layer_state(1, True)
    artifact.set_layer_state(2, True)

    rom.setFileByName(file_name, EntityFile.build(parsed_file))

    # Fault Line
    file_name, parsed_file = get_entity_file(rom, "Arcterra", "Fault Line")

    knocked_down_pillar = EntityFile.get_entity(parsed_file, 13)
    knocked_down_pillar.set_layer_state(1, False)
    knocked_down_pillar.set_layer_state(2, False)

    rom.setFileByName(file_name, EntityFile.build(parsed_file))


def _patch_both_escape_layers(rom: NintendoDSRom) -> None:
    ROOMS_TO_PATCH = {
        "Alinos": {
            "Alinos Gateway": [],
            "Alinos Perch": [0, 8, 10],  # layer 0 Guardian spawns
            "Council Chamber": [],
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
            "Stasis Bunker": [],
            "VDO Gateway": [],
            "Weapons Complex": [],
        },
        "Arcterra": {
            "Drip Moat": [],
            "Fault Line": [73],  # Disabled ship deck portal
            "Frost Labyrinth": [],
            "Ice Hive": [],
            "Sanctorus": [],
            "Subterranean": [],
        },
    }
    for area_name, room_names in ROOMS_TO_PATCH.items():
        for room_name, skipped_entities in room_names.items():
            file_name, parsed_file = get_entity_file(rom, area_name, room_name)
            for entity in parsed_file.entities:
                # Skip modifying any entities in this list
                if entity.entity_id in skipped_entities:
                    continue
                # Ensure entities on layer 0 are loaded on layer 1 (during escape) and layer 2 (post escape)
                elif entity.layer_state(0) is True:
                    entity.set_layer_state(1, True)
                    entity.set_layer_state(2, True)

            rom.setFileByName(file_name, EntityFile.build(parsed_file))
