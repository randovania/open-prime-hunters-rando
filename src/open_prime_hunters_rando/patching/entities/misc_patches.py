from typing import TYPE_CHECKING

from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.parsing.formats.entities.entity_types.area_volume import AreaVolume
from open_prime_hunters_rando.parsing.formats.entities.entity_types.object import Object
from open_prime_hunters_rando.parsing.formats.entities.entity_types.trigger_volume import TriggerVolume
from open_prime_hunters_rando.parsing.formats.entities.enum import Message

if TYPE_CHECKING:
    from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity


def misc_patches(file_manager: FileManager) -> None:
    _disable_message_prompts(file_manager)
    _move_data_shrine_01_fight_trigger(file_manager)
    _add_area_intro_message_oubliette_gateway(file_manager)


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
                entity: Entity = entity_file.get_entity(message_prompt)
                assert isinstance(entity, TriggerVolume | AreaVolume)
                entity.active = False


def _move_data_shrine_01_fight_trigger(file_manager: FileManager) -> None:
    entity_file = file_manager.get_entity_file("Celestial Archives", "Data Shrine 01")

    # Fight normally starts by scanning the Artifact Shield
    artifact_shield = entity_file.get_entity(48, Object)
    artifact_shield.scan_message_target = -1
    artifact_shield.scan_message = Message.NONE

    # Move the fight trigger to the scan below the Artifact Shield
    lower_scan = entity_file.get_entity(52, Object)
    lower_scan.scan_message_target = 43
    lower_scan.scan_message = Message.TRIGGER


def _add_area_intro_message_oubliette_gateway(file_manager: FileManager) -> None:
    entity_file = file_manager.get_entity_file("Oubliette", "Oubliette Gateway")

    # Add the message overlay to the trigger that activates the camera sequence
    trigger = entity_file.get_entity(18, TriggerVolume)
    trigger.child_message = Message.SHOW_OVERLAY
    trigger.child_message_param1 = 80
    trigger.child_message_param2 = 90
