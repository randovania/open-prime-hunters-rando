from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.entities.entity_type import EntityFile, Message
from open_prime_hunters_rando.level_data import get_entity_file


def static_patches(rom: NintendoDSRom) -> None:
    _disable_high_ground_force_field(rom)
    _disable_celestial_gateway_prompts(rom)
    _disable_fan_room_beta_popup(rom)
    _disable_new_arrival_registration_cutscenes(rom)
    _disable_sic_transit_force_field(rom)
    _disable_escape_sequences_and_layers(rom)


def _disable_high_ground_force_field(rom: NintendoDSRom) -> None:
    file_name, parsed_file = get_entity_file(rom, "Alinos", "High Ground")

    # Disable the force field in the floor (normally requires defeating Slench 1)
    trigger_volume = EntityFile.get_entity(parsed_file, 37)
    trigger_volume.data.parent_id = 0
    trigger_volume.data.parent_message = Message.NONE

    rom.setFileByName(file_name, EntityFile.build(parsed_file))


def _disable_celestial_gateway_prompts(rom: NintendoDSRom) -> None:
    file_name, parsed_file = get_entity_file(rom, "Celestial Archives", "Celestial Gateway")

    # Disable the message prompts
    for entity_id in [8, 24]:
        message_prompt = EntityFile.get_entity(parsed_file, entity_id)
        message_prompt.data.active = False

    rom.setFileByName(file_name, EntityFile.build(parsed_file))


def _disable_fan_room_beta_popup(rom: NintendoDSRom) -> None:
    file_name, parsed_file = get_entity_file(rom, "Celestial Archives", "Fan Room Beta")

    prompt = EntityFile.get_entity(parsed_file, 8)
    prompt.data.active = False

    rom.setFileByName(file_name, EntityFile.build(parsed_file))


def _disable_new_arrival_registration_cutscenes(rom: NintendoDSRom) -> None:
    file_name, parsed_file = get_entity_file(rom, "Celestial Archives", "New Arrival Registration")

    # Disable the first force field cutscene and force field, scans are now always active
    trigger_volume = EntityFile.get_entity(parsed_file, 34)
    trigger_volume.data.parent_id = 0

    # Disable the cutscene for deactivating the shield
    shield_key = EntityFile.get_entity(parsed_file, 49)
    shield_key.data.notify_entity_id = 31
    shield_key.data.collected_message = Message.SET_ACTIVE

    # Disable the second force field cutscene by linking directly to the Greater Ithrak enemy spawn
    artifact = EntityFile.get_entity(parsed_file, 19)
    artifact.data.message1_target = 53
    artifact.data.message1 = Message.TRIGGER

    rom.setFileByName(file_name, EntityFile.build(parsed_file))


def _disable_sic_transit_force_field(rom: NintendoDSRom) -> None:
    file_name, parsed_file = get_entity_file(rom, "Arcterra", "Sic Transit")

    # Disable the force field by the Magmaul door (normally requires defeating Slench 2)
    magmaul_door_force_field = EntityFile.get_entity(parsed_file, 64)
    magmaul_door_force_field.data.active = False

    rom.setFileByName(file_name, EntityFile.build(parsed_file))


def _disable_escape_sequences_and_layers(rom: NintendoDSRom) -> None:
    # Disable all escape triggers
    areas = ["Alinos", "Celestial Archives", "Vesper Defense Outpost", "Arcterra"]
    stronghold_voids = ["A", "B"]
    for area in areas:
        for stronghold_void in stronghold_voids:
            file_name, parsed_file = get_entity_file(rom, area, f"Stronghold Void {stronghold_void}")

            escape_trigger = EntityFile.get_entity(parsed_file, 5)
            escape_trigger.data.active = False

            rom.setFileByName(file_name, EntityFile.build(parsed_file))

    # Modify layer masks for entity files that need extra work
    # Echo Hall
    file_name, parsed_file = get_entity_file(rom, "Alinos", "Echo Hall")

    force_field = EntityFile.get_entity(parsed_file, 66)
    force_field.data.active = False

    rom.setFileByName(file_name, EntityFile.build(parsed_file))

    # Alinos Perch
    file_name, parsed_file = get_entity_file(rom, "Alinos", "Alinos Perch")

    second_pass_door = EntityFile.get_entity(parsed_file, 5)
    second_pass_door.set_layer_state(1, False)
    second_pass_door.set_layer_state(2, False)

    rom.setFileByName(file_name, EntityFile.build(parsed_file))

    # High Ground
    file_name, parsed_file = get_entity_file(rom, "Alinos", "High Ground")

    first_pass_bottom_door = EntityFile.get_entity(parsed_file, 15)
    first_pass_bottom_door.set_layer_state(3, True)

    second_pass_bottom_doors = [56, 72]
    for door in second_pass_bottom_doors:
        entity = EntityFile.get_entity(parsed_file, door)
        for layer in range(1, 4):
            entity.set_layer_state(layer, False)

    rom.setFileByName(file_name, EntityFile.build(parsed_file))

    # Elder Passage
    file_name, parsed_file = get_entity_file(rom, "Alinos", "Elder Passage")

    second_pass_doors = [11, 18]
    for door in second_pass_doors:
        entity = EntityFile.get_entity(parsed_file, door)
        for layer in range(1, 3):
            entity.set_layer_state(layer, False)

    disabled_portal_switch = EntityFile.get_entity(parsed_file, 21)
    disabled_portal_switch.set_layer_state(1, False)

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

    # Synergy Core
    file_name, parsed_file = get_entity_file(rom, "Celestial Archives", "Synergy Core")

    disabled_portal_switch = EntityFile.get_entity(parsed_file, 47)
    disabled_portal_switch.set_layer_state(1, False)

    rom.setFileByName(file_name, EntityFile.build(parsed_file))

    # Ascension
    file_name, parsed_file = get_entity_file(rom, "Vesper Defense Outpost", "Ascension")

    disabled_portal_switch = EntityFile.get_entity(parsed_file, 38)
    disabled_portal_switch.set_layer_state(1, False)

    rom.setFileByName(file_name, EntityFile.build(parsed_file))

    # Weapons Complex
    file_name, parsed_file = get_entity_file(rom, "Vesper Defense Outpost", "Weapons Complex")

    disabled_portal_switch = EntityFile.get_entity(parsed_file, 78)
    disabled_portal_switch.set_layer_state(1, False)

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

    # Modify the rest of the rooms
    ROOMS_TO_PATCH = {
        "Alinos": [
            "Alinos Gateway",
            "Alinos Perch",
            "Council Chamber",
            "Crash Site",
            "Echo Hall",
            "Elder Passage",
            "High Ground",
            "Piston Cave",
            "Processor Core",
        ],
        "Celestial Archives": [
            "Celestial Gateway",
            "Data Shrine 01",
            "Data Shrine 03",
            "Docking Bay",
            "Incubation Vault 01",
            "Incubation Vault 02",
            "New Arrival Registration",
            "Tetra Vista",
        ],
        "Vesper Defense Outpost": [
            "Ascension",
            "Compression Chamber",
            "Cortex CPU",
            "Fuel Stack",
            "Stasis Bunker",
            "VDO Gateway",
            "Weapons Complex",
        ],
        "Arcterra": [
            "Drip Moat",
            "Fault Line",
            "Frost Labyrinth",
            "Ice Hive",
            "Sanctorus",
            "Subterranean",
        ],
    }
    for area, rooms in ROOMS_TO_PATCH.items():
        for room in rooms:
            file_name, parsed_file = get_entity_file(rom, area, room)
            parsed_file = EntityFile.parse(rom.getFileByName(file_name))

            for entity in parsed_file.entities:
                # Ensure entities on layer 0 are loaded on layer 1 (during escape) and layer 2 (post escape)
                if entity.layer_state(0) is True:
                    entity.set_layer_state(1, True)
                    entity.set_layer_state(2, True)

            rom.setFileByName(file_name, EntityFile.build(parsed_file))
