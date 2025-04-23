from open_prime_hunters_rando.entities.entity_type import DoorType, Message
from open_prime_hunters_rando.file_manager import FileManager


def static_patches(file_manager: FileManager) -> None:
    _disable_boss_force_fields(file_manager)
    _disable_message_prompts(file_manager)
    _disable_new_arrival_registration_cutscenes(file_manager)
    _remove_elder_passage_top_lock_and_force_field(file_manager)
    _disable_alimbic_garden_cutscene(file_manager)
    _disable_fault_line_imperialist_cutscene(file_manager)
    _patch_sic_transit_inner_door(file_manager)


def _disable_boss_force_fields(file_manager: FileManager) -> None:
    boss_force_fields = [
        ("Alinos", "High Ground", 10),
        ("Vesper Defense Outpost", "Weapons Complex", 31),
        ("Arcterra", "Sic Transit", 64),
    ]
    for area_name, room_name, force_field in boss_force_fields:
        entity_file = file_manager.get_entity_file(area_name, room_name)
        entity = entity_file.get_entity(force_field)
        if entity.entity_id == 10:
            entity.set_layer_state(0, False)
            entity.set_layer_state(3, False)
        else:
            entity.data.active = False


def _disable_message_prompts(file_manager: FileManager) -> None:
    message_prompts_per_room = {
        "Celestial Archives": {
            "Celestial Gateway": [8, 24],  # Scan Visor and Enter Ship
            "Data Shrine 01": [54, 56],  # Unknown ship and Enter Morph Ball
            "Fan Room Beta": [8],  # Slench presence
        }
    }
    for area_name, room_names in message_prompts_per_room.items():
        for room_name, message_prompts in room_names.items():
            entity_file = file_manager.get_entity_file(area_name, room_name)
            for message_prompt in message_prompts:
                entity = entity_file.get_entity(message_prompt)
                entity.data.active = False


def _disable_new_arrival_registration_cutscenes(file_manager: FileManager) -> None:
    entity_file = file_manager.get_entity_file("Celestial Archives", "New Arrival Registration")

    # Disable the first force field cutscene and force field, scans are now always active
    trigger_volume = entity_file.get_entity(34)
    trigger_volume.data.parent_id = 0

    # Disable the cutscene for deactivating the shield
    shield_key = entity_file.get_entity(49)
    shield_key.data.notify_entity_id = 31
    shield_key.data.collected_message = Message.SET_ACTIVE

    # Disable the second force field cutscene by linking directly to the Greater Ithrak enemy spawn
    artifact = entity_file.get_entity(19)
    artifact.data.message1_target = 53
    artifact.data.message1 = Message.TRIGGER


def _remove_elder_passage_top_lock_and_force_field(file_manager: FileManager) -> None:
    entity_file = file_manager.get_entity_file("Alinos", "Elder Passage")
    trigger_volume = entity_file.get_entity(25)
    trigger_volume.data.parent_message = Message.NONE

    force_field = entity_file.get_entity(39)
    force_field.set_layer_state(0, False)
    force_field.set_layer_state(3, False)


def _disable_alimbic_garden_cutscene(file_manager: FileManager) -> None:
    entity_file = file_manager.get_entity_file("Alinos", "Alimbic Gardens")
    trigger_volume = entity_file.get_entity(7)
    trigger_volume.data.active = False


def _disable_fault_line_imperialist_cutscene(file_manager: FileManager) -> None:
    entity_file = file_manager.get_entity_file("Arcterra", "Fault Line")
    imperialist = entity_file.get_entity(46)
    imperialist.data.notify_entity_id = 0
    imperialist.data.collected_message = Message.NONE


def _patch_sic_transit_inner_door(file_manager: FileManager) -> None:
    entity_file = file_manager.get_entity_file("Arcterra", "Sic Transit")
    door = entity_file.get_entity(24)
    door.data.door_type = DoorType.THIN
