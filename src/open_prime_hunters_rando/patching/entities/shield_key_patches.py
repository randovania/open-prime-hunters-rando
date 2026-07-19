import copy

from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.parsing.formats.entities.entity_types.area_volume import AreaVolume
from open_prime_hunters_rando.parsing.formats.entities.entity_types.artifact import Artifact
from open_prime_hunters_rando.parsing.formats.entities.entity_types.camera_sequence import CameraSequence
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemy_spawn import EnemySpawn
from open_prime_hunters_rando.parsing.formats.entities.entity_types.trigger_volume import (
    TriggerVolume,
    TriggerVolumeType,
)
from open_prime_hunters_rando.parsing.formats.entities.enum import Message


def patch_shield_key_rooms(file_manager: FileManager) -> None:
    _high_ground(file_manager)
    _elder_passage(file_manager)
    _piston_cave(file_manager)
    _council_chamber(file_manager)
    _data_shrine_01(file_manager)
    _data_shrine_03(file_manager)
    _synergy_core(file_manager)
    _new_arrival_registration(file_manager)
    _docking_bay(file_manager)
    _weapons_complex(file_manager)
    _compression_chamber(file_manager)
    _fuel_stack(file_manager)
    _stasis_bunker(file_manager)
    _ice_hive(file_manager)
    _sic_transit(file_manager)
    _subterranean(file_manager)
    _sanctorus(file_manager)
    _fault_line(file_manager)


def _high_ground(file_manager: FileManager) -> None:
    high_ground = file_manager.get_entity_file("Alinos", "High Ground")

    # Only move the plaform after the artifact is collected
    artifact = high_ground.get_entity(24, Artifact)
    artifact.message1_target = 94
    artifact.message1 = Message.TRIGGER
    artifact.message2_target = -1
    artifact.message2 = Message.NONE
    artifact.message3_target = -1
    artifact.message3 = Message.NONE

    spire2 = high_ground.get_entity(60, EnemySpawn)

    # Move the messages that unlock the doors to a new trigger that activates after Spire is defeated
    unlocking_trigger = TriggerVolume.create(
        node_name="rmMain",
        layer_state=spire2.layer_state,
        subtype=TriggerVolumeType.AUTOMATIC,
        active=False,
        parent_id=17,
        parent_message=Message.UNLOCK,
        child_id=56,
        child_message=Message.UNLOCK_CONNECTORS,
    )
    high_ground.append_entity(unlocking_trigger)

    # Add a new trigger that activates the artifact and the door unlocking trigger
    post_spire_trigger = TriggerVolume.create(
        node_name="rmMain",
        layer_state=spire2.layer_state,
        subtype=TriggerVolumeType.AUTOMATIC,
        active=False,
        parent_id=81,
        parent_message=Message.ACTIVATE,
        child_id=unlocking_trigger.entity_id,
        child_message=Message.ACTIVATE,
    )
    high_ground.append_entity(post_spire_trigger)

    # Replace the message thats activates the artifact with moving the item spawner
    # and activate the new post-Spire trigger
    spire2.message1_target = 81
    spire2.message1 = Message.MOVE_ITEM_SPAWNER
    spire2.message2_target = post_spire_trigger.entity_id
    spire2.message2 = Message.ACTIVATE

    # Delay setting the checkpoint to prevent the shield key cutscene from not reactivating if shuffled
    checkpoint = high_ground.get_entity(86, AreaVolume)
    checkpoint.message_delay = 180


def _elder_passage(file_manager: FileManager) -> None:
    elder_passage = file_manager.get_entity_file("Alinos", "Elder Passage")

    # Remove the messages that unlocks the door and sets the state bit
    artifact = elder_passage.get_entity(4, Artifact)
    artifact.message1_target = -1
    artifact.message1 = Message.NONE
    artifact.message2_target = -1
    artifact.message2 = Message.NONE

    # Spire exit camera sequence now sets the state bit
    camera_sequence = elder_passage.get_entity(26, CameraSequence)
    camera_sequence.end_message_target_id = 40
    camera_sequence.end_message = Message.TRIGGER

    # Remove the message that locks the lower door
    locking_trigger = elder_passage.get_entity(40, TriggerVolume)
    locking_trigger.child_id = -1
    locking_trigger.child_message = Message.NONE


def _piston_cave(file_manager: FileManager) -> None:
    piston_cave = file_manager.get_entity_file("Alinos", "Piston Cave")

    # Remove the messages that lock the doors
    trigger = piston_cave.get_entity(82, TriggerVolume)
    trigger.parent_id = -1
    trigger.parent_message = Message.NONE
    trigger.child_id = -1
    trigger.child_message = Message.NONE

    # Remove the messages that unlock the doors
    artifact = piston_cave.get_entity(38, Artifact)
    artifact.message1_target = -1
    artifact.message1 = Message.NONE
    artifact.message2_target = -1
    artifact.message2 = Message.NONE


def _council_chamber(file_manager: FileManager) -> None:
    council_chamber = file_manager.get_entity_file("Alinos", "Council Chamber")

    # Delay setting the checkpoint to prevent the shield key cutscene from not reactivating if shuffled
    checkpoint = council_chamber.get_entity(67, AreaVolume)
    checkpoint.message_delay = 180


def _data_shrine_01(file_manager: FileManager) -> None:
    data_shrine_01 = file_manager.get_entity_file("Celestial Archives", "Data Shrine 01")

    # Remove the message that unlocks the doors
    artifact = data_shrine_01.get_entity(2, Artifact)
    artifact.message1_target = -1
    artifact.message1 = Message.NONE

    # Add a new trigger that unlocks the doors after the fight
    door_unlocking_trigger = TriggerVolume.create(
        node_name=artifact.node_name,
        layer_state=artifact.layer_state,
        subtype=TriggerVolumeType.AUTOMATIC,
        active=False,
        parent_id=8,
        parent_message=Message.UNLOCK,
        child_id=9,
        child_message=Message.UNLOCK,
    )
    data_shrine_01.append_entity(door_unlocking_trigger)

    # Activate the new trigger after the shield key cutscene
    camera_sequence = data_shrine_01.get_entity(10, CameraSequence)
    camera_sequence.end_message_target_id = door_unlocking_trigger.entity_id
    camera_sequence.end_message = Message.ACTIVATE

    # Delay setting the checkpoint to prevent the shield key cutscene from not reactivating if shuffled
    checkpoint = data_shrine_01.get_entity(50, AreaVolume)
    checkpoint.message_delay = 180


def _data_shrine_03(file_manager: FileManager) -> None:
    data_shrine_03 = file_manager.get_entity_file("Celestial Archives", "Data Shrine 03")

    # Remove the message that unlocks the doors
    artifact = data_shrine_03.get_entity(2, Artifact)
    artifact.message1_target = -1
    artifact.message1 = Message.NONE

    # Add a new trigger that unlocks the doors after the fight
    door_unlocking_trigger = TriggerVolume.create(
        node_name=artifact.node_name,
        layer_state=artifact.layer_state,
        subtype=TriggerVolumeType.AUTOMATIC,
        active=False,
        parent_id=4,
        parent_message=Message.UNLOCK,
        child_id=7,
        child_message=Message.UNLOCK,
    )
    data_shrine_03.append_entity(door_unlocking_trigger)

    # Activate the new trigger after the shield key cutscene
    camera_sequence = data_shrine_03.get_entity(42, CameraSequence)
    camera_sequence.end_message_target_id = door_unlocking_trigger.entity_id
    camera_sequence.end_message = Message.ACTIVATE

    # Delay setting the checkpoint to prevent the shield key cutscene from not reactivating if shuffled
    checkpoint = data_shrine_03.get_entity(50, AreaVolume)
    checkpoint.message_delay = 180


def _synergy_core(file_manager: FileManager) -> None:
    synergy_core = file_manager.get_entity_file("Celestial Archives", "Synergy Core")

    # Prevent the doors from locking
    locking_trigger = synergy_core.get_entity(28, TriggerVolume)
    locking_trigger.active = False

    # Enable the buttons by default
    button_activation_triggers = [59, 60]
    for activation_trigger in button_activation_triggers:
        trigger = synergy_core.get_entity(activation_trigger, TriggerVolume)
        trigger.subtype = TriggerVolumeType.AUTOMATIC

    # Remove the messages from the Artifact
    artifact = synergy_core.get_entity(3, Artifact)
    artifact.message1_target = -1
    artifact.message1 = Message.NONE

    # Delay setting the checkpoints to prevent the shield key cutscenes from not reactivating if shuffled
    checkpoints = [50, 51]
    for checkpoint_id in checkpoints:
        checkpoint = synergy_core.get_entity(checkpoint_id, AreaVolume)
        checkpoint.message_delay = 180


def _new_arrival_registration(file_manager: FileManager) -> None:
    new_arrival_registration = file_manager.get_entity_file("Celestial Archives", "New Arrival Registration")

    # Delay setting the checkpoint to prevent the shield key cutscene from not reactivating if shuffled
    checkpoint = new_arrival_registration.get_entity(35, AreaVolume)
    checkpoint.message_delay = 180


def _docking_bay(file_manager: FileManager) -> None:
    docking_bay = file_manager.get_entity_file("Celestial Archives", "Docking Bay")

    # Delay setting the checkpoint to prevent the shield key cutscene from not reactivating if shuffled
    checkpoint = docking_bay.get_entity(21, AreaVolume)
    checkpoint.message_delay = 180


def _weapons_complex(file_manager: FileManager) -> None:
    weapons_complex = file_manager.get_entity_file("Vesper Defense Outpost", "Weapons Complex")

    # Activate the platform after spawning the first shield key
    spawn_first_key = weapons_complex.get_entity(62, TriggerVolume)
    spawn_first_key.child_message = Message.SET_TRIGGER_STATE
    spawn_first_key.child_message_param1 = 20

    # Remove the cutscene for the first artifact shield and unlock it directly
    first_shield_key_trigger = weapons_complex.get_entity(101, TriggerVolume)
    first_shield_key_trigger.parent_id = 63
    first_shield_key_trigger.parent_message = Message.SET_ACTIVE

    # Delay setting the checkpoints to prevent the shield key cutscenes from not reactivating if shuffled
    checkpoints = [46, 82]
    for checkpoint_id in checkpoints:
        checkpoint = weapons_complex.get_entity(checkpoint_id, AreaVolume)
        checkpoint.message_delay = 180


def _compression_chamber(file_manager: FileManager) -> None:
    compression_chamber = file_manager.get_entity_file("Vesper Defense Outpost", "Compression Chamber")

    # Delay setting the checkpoint to prevent the shield key cutscene from not reactivating if shuffled
    checkpoint = compression_chamber.get_entity(44, AreaVolume)
    checkpoint.message_delay = 180


def _fuel_stack(file_manager: FileManager) -> None:
    fuel_stack = file_manager.get_entity_file("Vesper Defense Outpost", "Fuel Stack")

    # Delay setting the checkpoint to prevent the shield key cutscene from not reactivating if shuffled
    checkpoint = fuel_stack.get_entity(7, AreaVolume)
    checkpoint.message_delay = 180


def _stasis_bunker(file_manager: FileManager) -> None:
    stasis_bunker = file_manager.get_entity_file("Vesper Defense Outpost", "Stasis Bunker")

    # Lock the doors when the first artifact is collected instead of when entering the room
    first_artifact = stasis_bunker.get_entity(5, Artifact)
    first_artifact.message2_target = 1
    first_artifact.message2 = Message.LOCK
    first_artifact.message3_target = 2
    first_artifact.message3 = Message.LOCK

    # Remove the message that unlocks the doors from the second artifact
    second_artifact = stasis_bunker.get_entity(4, Artifact)
    second_artifact.message1_target = -1
    second_artifact.message1 = Message.NONE

    # Change the trigger that locked the doors to unlock the doors after the second shield key spawns
    door_locking_trigger = stasis_bunker.get_entity(34, TriggerVolume)
    door_locking_trigger.subtype = TriggerVolumeType.AUTOMATIC
    door_locking_trigger.active = False
    door_locking_trigger.parent_message = Message.UNLOCK
    door_locking_trigger.child_message = Message.UNLOCK

    # Activate the "new" trigger that unlocks the doors
    camera_sequence = stasis_bunker.get_entity(33, CameraSequence)
    camera_sequence.end_message_target_id = 34
    camera_sequence.end_message = Message.ACTIVATE

    # Delay setting the checkpoint to prevent the shield key cutscene from not reactivating if shuffled
    checkpoint = stasis_bunker.get_entity(70, AreaVolume)
    checkpoint.message_delay = 255


def _ice_hive(file_manager: FileManager) -> None:
    ice_hive = file_manager.get_entity_file("Arcterra", "Ice Hive")

    # Delay setting the checkpoint to prevent the shield key cutscene from not reactivating if shuffled
    checkpoint = ice_hive.get_entity(170, AreaVolume)
    checkpoint.message_delay = 180


def _sic_transit(file_manager: FileManager) -> None:
    sic_transit = file_manager.get_entity_file("Arcterra", "Sic Transit")

    # Remove the locking messages from the artifact
    artifact = sic_transit.get_entity(35, Artifact)
    artifact.message1_target = -1
    artifact.message1 = Message.NONE
    artifact.message2_target = -1
    artifact.message2 = Message.NONE

    # Unlock the doors after the shield key spawns
    door_locking_trigger = sic_transit.get_entity(20, TriggerVolume)

    unlocking_trigger = copy.deepcopy(door_locking_trigger)
    unlocking_trigger.parent_message = Message.UNLOCK
    unlocking_trigger.child_message = Message.UNLOCK
    sic_transit.append_entity(unlocking_trigger)

    camera_sequence = sic_transit.get_entity(23, CameraSequence)
    camera_sequence.end_message_target_id = unlocking_trigger.entity_id
    camera_sequence.end_message = Message.ACTIVATE

    # Delay setting the checkpoint to prevent the shield key cutscene from not reactivating if shuffled
    checkpoint = sic_transit.get_entity(61, AreaVolume)
    checkpoint.message_delay = 180


def _subterranean(file_manager: FileManager) -> None:
    subterranean = file_manager.get_entity_file("Arcterra", "Subterranean")

    # Delay setting the checkpoint to prevent the shield key cutscene from not reactivating if shuffled
    checkpoint = subterranean.get_entity(55, AreaVolume)
    checkpoint.message_delay = 180


def _sanctorus(file_manager: FileManager) -> None:
    sanctorus = file_manager.get_entity_file("Arcterra", "Sanctorus")

    # Move the message that activates the Guardians to the shield key activation camera sequence
    artifact = sanctorus.get_entity(7, Artifact)
    artifact.message1_target = -1
    artifact.message1 = Message.NONE

    camera_sequence = sanctorus.get_entity(39, CameraSequence)
    camera_sequence.end_message_target_id = 38
    camera_sequence.end_message = Message.ACTIVATE

    # Delay setting the checkpoint to prevent the shield key cutscene from not reactivating if shuffled
    checkpoint = sanctorus.get_entity(32, AreaVolume)
    checkpoint.message_delay = 180


def _fault_line(file_manager: FileManager) -> None:
    fault_line = file_manager.get_entity_file("Arcterra", "Fault Line")

    # Delay setting the checkpoint to prevent the shield key cutscene from not reactivating if shuffled
    checkpoint = fault_line.get_entity(70, AreaVolume)
    checkpoint.message_delay = 180
