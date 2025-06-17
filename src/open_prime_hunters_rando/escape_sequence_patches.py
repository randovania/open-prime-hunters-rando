from open_prime_hunters_rando.file_manager import FileManager


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
                entity = entity_file.get_entity(escape_trigger)
                entity.set_layer_state(1, False)


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
                entity = entity_file.get_entity(portal_entity)
                entity.set_layer_state(1, False)


def _patch_specific_rooms(file_manager: FileManager) -> None:
    # High Ground
    entity_file = file_manager.get_entity_file("Alinos", "High Ground")

    first_pass_bottom_door = entity_file.get_entity(15)
    first_pass_bottom_door.set_layer_state(3, True)

    second_pass_bottom_doors = [56, 72]
    for door in second_pass_bottom_doors:
        entity = entity_file.get_entity(door)
        for layer in range(1, 4):
            entity.set_layer_state(layer, False)

    force_fields = [74, 77]
    for force_field in force_fields:
        entity = entity_file.get_entity(force_field)
        entity.set_layer_state(3, True)

    portals = [57, 58]
    for portal in portals:
        entity = entity_file.get_entity(portal)
        entity.set_layer_state(3, True)

    hunters = [85, 95]
    for hunter in hunters:
        entity = entity_file.get_entity(hunter)
        entity.set_layer_state(1, True)

    # Elder Passage
    entity_file = file_manager.get_entity_file("Alinos", "Elder Passage")

    second_pass_doors = [11, 18]
    for door in second_pass_doors:
        entity = entity_file.get_entity(door)
        for layer in range(1, 3):
            entity.set_layer_state(layer, False)

    # Alinos Perch
    entity_file = file_manager.get_entity_file("Alinos", "Alinos Perch")

    second_pass_door = entity_file.get_entity(5)
    second_pass_door.set_layer_state(1, False)
    second_pass_door.set_layer_state(2, False)

    # Data Shrine 01
    entity_file = file_manager.get_entity_file("Celestial Archives", "Data Shrine 01")

    second_pass_door = entity_file.get_entity(37)
    second_pass_door.set_layer_state(1, False)
    second_pass_door.set_layer_state(2, False)

    # Frost Labyrinth
    entity_file = file_manager.get_entity_file("Arcterra", "Frost Labyrinth")

    force_field = entity_file.get_entity(5)
    second_pass_door.set_layer_state(0, False)

    # Arcterra Gateway
    entity_file = file_manager.get_entity_file("Arcterra", "Arcterra Gateway")

    # Landing camera
    camera_sequence = entity_file.get_entity(36)
    camera_sequence.set_layer_state(1, True)
    camera_sequence.set_layer_state(2, True)

    # Teleporter triggers
    trigger_volumes = [5, 39]
    for trigger_volume in trigger_volumes:
        entity = entity_file.get_entity(trigger_volume)
        entity.set_layer_state(1, True)

    # Ice Hive
    entity_file = file_manager.get_entity_file("Arcterra", "Ice Hive")

    entrance_jump_pad = entity_file.get_entity(65)
    entrance_jump_pad.set_layer_state(1, False)
    entrance_jump_pad.set_layer_state(2, False)

    # Sic Transit
    entity_file = file_manager.get_entity_file("Arcterra", "Sic Transit")

    first_pass_inner_door = entity_file.get_entity(24)
    first_pass_inner_door.set_layer_state(1, True)
    first_pass_inner_door.set_layer_state(2, True)

    second_pass_inner_door = entity_file.get_entity(11)
    second_pass_inner_door.set_layer_state(1, False)
    second_pass_inner_door.set_layer_state(2, False)

    artifact = entity_file.get_entity(35)
    artifact.set_layer_state(1, True)
    artifact.set_layer_state(2, True)

    # Fault Line
    entity_file = file_manager.get_entity_file("Arcterra", "Fault Line")

    knocked_down_pillar = entity_file.get_entity(13)
    knocked_down_pillar.set_layer_state(1, False)
    knocked_down_pillar.set_layer_state(2, False)


def _patch_both_escape_layers(file_manager: FileManager) -> None:
    ROOMS_TO_PATCH = {
        "Alinos": {
            "Alinos Gateway": [],
            "Alinos Perch": [],
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
                elif entity.layer_state(0) is True:
                    entity.set_layer_state(1, True)
                    entity.set_layer_state(2, True)
