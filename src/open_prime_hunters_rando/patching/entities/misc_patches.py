from typing import TYPE_CHECKING

from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.parsing.formats.entities.entity_types.area_volume import AreaVolume
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemy_spawn import EnemySpawn
from open_prime_hunters_rando.parsing.formats.entities.entity_types.force_field import ForceField
from open_prime_hunters_rando.parsing.formats.entities.entity_types.object import Object
from open_prime_hunters_rando.parsing.formats.entities.entity_types.trigger_volume import TriggerVolume
from open_prime_hunters_rando.parsing.formats.entities.enum import Message

if TYPE_CHECKING:
    from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity


def misc_patches(file_manager: FileManager) -> None:
    _disable_message_prompts(file_manager)
    _remove_elder_passage_top_lock_and_force_field(file_manager)
    _move_data_shrine_01_fight_trigger(file_manager)
    _save_vram_ice_hive(file_manager)


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


def _remove_elder_passage_top_lock_and_force_field(file_manager: FileManager) -> None:
    entity_file = file_manager.get_entity_file("Alinos", "Elder Passage")
    trigger_volume = entity_file.get_entity(25, TriggerVolume)
    trigger_volume.parent_message = Message.NONE

    force_field = entity_file.get_entity(39, ForceField)
    force_field.layer_state[0] = False
    force_field.layer_state[3] = False


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


def _save_vram_ice_hive(file_manager: FileManager) -> None:
    # Remove some entities to prevent VRAM overflow in large rooms
    entity_file = file_manager.get_entity_file("Arcterra", "Ice Hive")

    # Remove the Carnivorous Plants in the path under the Artifact
    to_remove = [33, 108, 111]
    for entity_id in to_remove:
        carnivorous_plant = entity_file.get_entity(entity_id, EnemySpawn)
        for layer in range(3):
            carnivorous_plant.layer_state[layer] = False
