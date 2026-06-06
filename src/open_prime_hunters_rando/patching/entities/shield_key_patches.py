import copy

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3
from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.parsing.formats.entities.entity_types.artifact import Artifact
from open_prime_hunters_rando.parsing.formats.entities.entity_types.camera_sequence import CameraSequence
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemy_spawn import EnemySpawn
from open_prime_hunters_rando.parsing.formats.entities.entity_types.item_spawn import ItemSpawn
from open_prime_hunters_rando.parsing.formats.entities.entity_types.trigger_volume import (
    TriggerVolume,
    TriggerVolumeType,
)
from open_prime_hunters_rando.parsing.formats.entities.enum import Message


def patch_shield_key_rooms(file_manager: FileManager) -> None:
    _high_ground(file_manager)
    _elder_passage(file_manager)
    _piston_cave(file_manager)
    _data_shrine_01(file_manager)
    _data_shrine_03(file_manager)
    _synergy_core(file_manager)
    _stasis_bunker(file_manager)
    _sic_transit(file_manager)


def _high_ground(file_manager: FileManager) -> None:
    high_ground = file_manager.get_entity_file("Alinos", "High Ground")

    # Only move the plaform when the Artifact is collected
    artifact = high_ground.get_entity(24, Artifact)
    artifact.message1_target = 94
    artifact.message1 = Message.TRIGGER
    artifact.message2_target = -1
    artifact.message2 = Message.NONE
    artifact.message3_target = -1
    artifact.message3 = Message.NONE

    # Move the Shield Key to Spire's spawn point to avoid having to add extra triggers to set the state bit
    shield_key = high_ground.get_entity(81, ItemSpawn)
    shield_key.position = Vec3(-0.05419921875, 11.60107421875, 9.8974609375)

    # Move the messages that unlock the doors to a new trigger that activates after Spire is defeated
    unlocking_trigger = TriggerVolume.create(
        node_name="rmMain",
        layer_state=shield_key.layer_state,
        subtype=TriggerVolumeType.AUTOMATIC,
        active=False,
        parent_id=17,
        parent_message=Message.UNLOCK,
        child_id=56,
        child_message=Message.UNLOCK_CONNECTORS,
    )

    high_ground.append_entity(unlocking_trigger)

    # Replace the message thats moves the item spawner to Spire's place of defeat with unlocking the doors
    spire = high_ground.get_entity(60, EnemySpawn)
    spire.message2_target = unlocking_trigger.entity_id
    spire.message2 = Message.ACTIVATE


def _elder_passage(file_manager: FileManager) -> None:
    elder_passage = file_manager.get_entity_file("Alinos", "Elder Passage")

    # Move the message that unlocks the doors from the Artifact to the Camera Sequence
    artifact = elder_passage.get_entity(4, Artifact)
    artifact.message1_target = -1
    artifact.message1 = Message.NONE

    camera_sequence = elder_passage.get_entity(26, CameraSequence)
    camera_sequence.end_message_target_id = 43
    camera_sequence.end_message = Message.ACTIVATE


def _piston_cave(file_manager: FileManager) -> None:
    piston_cave = file_manager.get_entity_file("Alinos", "Piston Cave")

    # Prevent the doors from locking
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


def _data_shrine_01(file_manager: FileManager) -> None:
    data_shrine_01 = file_manager.get_entity_file("Celestial Archives", "Data Shrine 01")

    # Move the message that unlocks the doors from the Artifact to the Camera Sequence
    artifact = data_shrine_01.get_entity(2, Artifact)
    artifact.message1_target = -1
    artifact.message1 = Message.NONE

    camera_sequence = data_shrine_01.get_entity(10, CameraSequence)
    camera_sequence.end_message_target_id = 21
    camera_sequence.end_message = Message.ACTIVATE


def _data_shrine_03(file_manager: FileManager) -> None:
    data_shrine_03 = file_manager.get_entity_file("Celestial Archives", "Data Shrine 03")

    # Move the message that unlocks the doors from the Artifact to the Camera Sequence
    artifact = data_shrine_03.get_entity(2, Artifact)
    artifact.message1_target = -1
    artifact.message1 = Message.NONE

    camera_sequence = data_shrine_03.get_entity(42, CameraSequence)
    camera_sequence.end_message_target_id = 22
    camera_sequence.end_message = Message.ACTIVATE

    # Move the Shield Key to the center of the room to avoid having to add extra triggers to set the state bit
    shield_key = data_shrine_03.get_entity(45, ItemSpawn)
    shield_key.position = Vec3(0.0, 3.7421875, 0.0)

    # Remove the message thats moves the item spawner to Kanden's place of defeat
    kanden = data_shrine_03.get_entity(3, EnemySpawn)
    kanden.message3_target = -1
    kanden.message3 = Message.NONE


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


def _stasis_bunker(file_manager: FileManager) -> None:
    stasis_bunker = file_manager.get_entity_file("Vesper Defense Outpost", "Stasis Bunker")

    # Lock the doors when the first Artifact is collected instead of when entering the room
    first_artifact = stasis_bunker.get_entity(5, Artifact)
    first_artifact.message2_target = 1
    first_artifact.message2 = Message.LOCK
    first_artifact.message3_target = 2
    first_artifact.message3 = Message.LOCK

    # Remove the message that unlocks the doors from the second Artifact
    second_artifact = stasis_bunker.get_entity(4, Artifact)
    second_artifact.message1_target = -1
    second_artifact.message1 = Message.NONE

    # Change the trigger that locked the doors to unlock the doors after the second Shield Key spawns
    door_locking_trigger = stasis_bunker.get_entity(34, TriggerVolume)
    door_locking_trigger.subtype = TriggerVolumeType.AUTOMATIC
    door_locking_trigger.active = False
    door_locking_trigger.parent_message = Message.UNLOCK
    door_locking_trigger.child_message = Message.UNLOCK

    # Activate the "new" trigger that unlocks the doors
    camera_sequence = stasis_bunker.get_entity(33, CameraSequence)
    camera_sequence.end_message_target_id = 34
    camera_sequence.end_message = Message.ACTIVATE


def _sic_transit(file_manager: FileManager) -> None:
    sic_transit = file_manager.get_entity_file("Arcterra", "Sic Transit")

    # Remove the locking messages from the Artifact
    artifact = sic_transit.get_entity(35, Artifact)
    artifact.message1_target = -1
    artifact.message1 = Message.NONE
    artifact.message2_target = -1
    artifact.message2 = Message.NONE

    # Unlock the doors after the Shield Key spawns
    door_locking_trigger = sic_transit.get_entity(20, TriggerVolume)

    unlocking_trigger = copy.deepcopy(door_locking_trigger)
    unlocking_trigger.parent_message = Message.UNLOCK
    unlocking_trigger.child_message = Message.UNLOCK

    sic_transit.append_entity(unlocking_trigger)

    camera_sequence = sic_transit.get_entity(23, CameraSequence)
    camera_sequence.end_message_target_id = unlocking_trigger.entity_id
    camera_sequence.end_message = Message.ACTIVATE
