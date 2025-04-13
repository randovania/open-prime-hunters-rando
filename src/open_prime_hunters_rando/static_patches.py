from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.entities.entity_type import EntityFile, Message
from open_prime_hunters_rando.level_data import get_entity_file


def static_patches(rom: NintendoDSRom) -> None:
    _disable_boss_force_fields(rom)
    _disable_message_prompts(rom)
    _disable_new_arrival_registration_cutscenes(rom)
    _disable_elder_passage_top_lock(rom)


def _disable_boss_force_fields(rom: NintendoDSRom) -> None:
    boss_force_fields = [
        ("Alinos", "High Ground", 10),
        ("Vesper Defense Outpost", "Weapons Complex", 31),
        ("Arcterra", "Sic Transit", 64),
    ]
    for area_name, room_name, force_field in boss_force_fields:
        file_name, parsed_file = get_entity_file(rom, area_name, room_name)
        entity = EntityFile.get_entity(parsed_file, force_field)
        if entity.entity_id == 10:
            entity.set_layer_state(0, False)
            entity.set_layer_state(3, False)
        else:
            entity.data.active = False

        rom.setFileByName(file_name, EntityFile.build(parsed_file))


def _disable_message_prompts(rom: NintendoDSRom) -> None:
    message_prompts_per_room = [
        ("Celestial Archives", "Celestial Gateway", [8, 24]),
        ("Celestial Archives", "Fan Room Beta", [8]),
    ]
    for area_name, room_name, message_prompts in message_prompts_per_room:
        file_name, parsed_file = get_entity_file(rom, area_name, room_name)
        for message_prompt in message_prompts:
            entity = EntityFile.get_entity(parsed_file, message_prompt)
            entity.data.active = False

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


def _disable_elder_passage_top_lock(rom: NintendoDSRom) -> None:
    file_name, parsed_file = get_entity_file(rom, "Alinos", "Elder Passage")
    trigger_volume = EntityFile.get_entity(parsed_file, 25)
    trigger_volume.data.parent_message = Message.NONE

    rom.setFileByName(file_name, EntityFile.build(parsed_file))
