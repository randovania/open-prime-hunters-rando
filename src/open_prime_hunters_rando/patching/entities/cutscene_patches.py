from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.parsing.formats.entities.entity_types.artifact import Artifact
from open_prime_hunters_rando.parsing.formats.entities.entity_types.item_spawn import ItemSpawn
from open_prime_hunters_rando.parsing.formats.entities.entity_types.object import Object
from open_prime_hunters_rando.parsing.formats.entities.entity_types.trigger_volume import TriggerVolume
from open_prime_hunters_rando.parsing.formats.entities.enum import Message


def remove_cutscenes(file_manager: FileManager) -> None:
    _alimbic_gardens(file_manager)
    _helm_room_scan_door(file_manager)
    _new_arrival_registration(file_manager)
    _fault_line_imperialist_tutorial(file_manager)


def _alimbic_gardens(file_manager: FileManager) -> None:
    alimbic_gardens = file_manager.get_entity_file("Alinos", "Alimbic Gardens")
    trigger_volume = alimbic_gardens.get_entity(7, TriggerVolume)
    trigger_volume.active = False


def _helm_room_scan_door(file_manager: FileManager) -> None:
    helm_room = file_manager.get_entity_file("Celestial Archives", "Helm Room")

    # Scan object that unlocks the door
    obj = helm_room.get_entity(9, Object)
    obj.scan_message_target = 8
    obj.scan_message = Message.UNLOCK

    # Trigger activates the cutscene showing the door
    trigger = helm_room.get_entity(17, TriggerVolume)
    trigger.active = False


def _new_arrival_registration(file_manager: FileManager) -> None:
    new_arrival_registration = file_manager.get_entity_file("Celestial Archives", "New Arrival Registration")

    # Disable the first force field cutscene and force field, scans are now always active
    trigger_volume = new_arrival_registration.get_entity(34, TriggerVolume)
    trigger_volume.parent_id = 0

    # Disable the cutscene for deactivating the shield
    shield_key = new_arrival_registration.get_entity(49, ItemSpawn)
    shield_key.notify_entity_id = 31
    shield_key.collected_message = Message.SET_ACTIVE

    # Disable the second force field cutscene by linking directly to the Greater Ithrak enemy spawn
    artifact = new_arrival_registration.get_entity(19, Artifact)
    artifact.message1_target = 53
    artifact.message1 = Message.TRIGGER


def _fault_line_imperialist_tutorial(file_manager: FileManager) -> None:
    fault_line = file_manager.get_entity_file("Arcterra", "Fault Line")
    imperialist = fault_line.get_entity(46, ItemSpawn)
    imperialist.notify_entity_id = 0
    imperialist.collected_message = Message.NONE
