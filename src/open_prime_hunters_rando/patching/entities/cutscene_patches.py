from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.parsing.formats.entities.entity_types.area_volume import AreaVolume
from open_prime_hunters_rando.parsing.formats.entities.entity_types.artifact import Artifact
from open_prime_hunters_rando.parsing.formats.entities.entity_types.camera_sequence import CameraSequence
from open_prime_hunters_rando.parsing.formats.entities.entity_types.item_spawn import ItemSpawn
from open_prime_hunters_rando.parsing.formats.entities.entity_types.object import Object
from open_prime_hunters_rando.parsing.formats.entities.entity_types.platform import Platform, PlatformFlags
from open_prime_hunters_rando.parsing.formats.entities.entity_types.player_spawn import PlayerSpawn
from open_prime_hunters_rando.parsing.formats.entities.entity_types.trigger_volume import TriggerVolume
from open_prime_hunters_rando.parsing.formats.entities.enum import Message


def remove_cutscenes(file_manager: FileManager, skip_planet_intros: bool) -> None:
    _alimbic_gardens(file_manager)
    _helm_room_scan_door(file_manager)
    _new_arrival_registration(file_manager)
    _fault_line_imperialist_tutorial(file_manager)

    if skip_planet_intros:
        _planet_intros(file_manager)


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


def _planet_intros(file_manager: FileManager) -> None:
    ship_landing_mapping = [
        ("Alinos", "Alinos Gateway", 1, 4, 6, 11),
        ("Celestial Archives", "Celestial Gateway", 0, 5, 7, 8),
        ("Vesper Defense Outpost", "VDO Gateway", 0, 6, 11, 9),
        ("Arcterra", "Arcterra Gateway", 0, 9, 36, 41),
        ("Oubliette", "Oubliette Gateway", 14, 0, 19, 20),
    ]

    for (
        area_name,
        room_name,
        player_spawn_id,
        ship_platform_id,
        camera_sequence_id,
        area_volume_id,
    ) in ship_landing_mapping:
        entity_file = file_manager.get_entity_file(area_name, room_name)

        # Activate the player spawn
        player_spawn = entity_file.get_entity(player_spawn_id, PlayerSpawn)
        player_spawn.active = 1

        # Force the ship to be landed on load
        ship = entity_file.get_entity(ship_platform_id, Platform)
        ship.platform_flags = PlatformFlags.BIT15

        # Disable the camera sequence
        camera_sequence = entity_file.get_entity(camera_sequence_id, CameraSequence)
        for layer in camera_sequence.active_layers:
            camera_sequence.layer_state[layer] = False

        # Disable the area volume that moves the ship
        area_volume = entity_file.get_entity(area_volume_id, AreaVolume)
        area_volume.active = False
