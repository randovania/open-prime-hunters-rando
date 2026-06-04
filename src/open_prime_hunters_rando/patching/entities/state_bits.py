import dataclasses
import enum

from open_prime_hunters_rando.parsing.common_types.volume import SphereVolumeType, TriggerVolumeFlags
from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.parsing.formats.entities.entity_types.item_spawn import ItemSpawn
from open_prime_hunters_rando.parsing.formats.entities.entity_types.trigger_volume import (
    TriggerVolume,
    TriggerVolumeType,
)


class UnlockMessage(enum.StrEnum):
    DOOR = "a DOOR was unlocked"
    SHIELD = "an ARTIFACT SHIELD was deactivated"
    FORCE_FIELD = "a FORCE FIELD was disabled"


@dataclasses.dataclass(frozen=True)
class ShieldKeyData:
    area_name: str
    room_name: str
    entity_id: int
    unlock_message: UnlockMessage


STATE_BIT_SHIELD_KEY_MAPPING: dict[int, ShieldKeyData] = {
    32: ShieldKeyData(
        area_name="Alinos",
        room_name="Echo Hall",
        entity_id=42,
        unlock_message=UnlockMessage.DOOR,
    ),
    33: ShieldKeyData(
        area_name="Alinos",
        room_name="Elder Passage",
        entity_id=29,
        unlock_message=UnlockMessage.SHIELD,
    ),
    34: ShieldKeyData(
        area_name="Alinos",
        room_name="High Ground",
        entity_id=81,
        unlock_message=UnlockMessage.SHIELD,
    ),
    35: ShieldKeyData(
        area_name="Alinos",
        room_name="Crash Site",
        entity_id=8,
        unlock_message=UnlockMessage.SHIELD,
    ),
    36: ShieldKeyData(
        area_name="Alinos",
        room_name="Council Chamber",
        entity_id=61,
        unlock_message=UnlockMessage.FORCE_FIELD,
    ),
    37: ShieldKeyData(
        area_name="Alinos",
        room_name="Piston Cave",
        entity_id=80,
        unlock_message=UnlockMessage.SHIELD,
    ),
    38: ShieldKeyData(
        area_name="Celestial Archives",
        room_name="Data Shrine 01",
        entity_id=46,
        unlock_message=UnlockMessage.SHIELD,
    ),
    39: ShieldKeyData(
        area_name="Celestial Archives",
        room_name="Data Shrine 03",
        entity_id=45,
        unlock_message=UnlockMessage.DOOR,
    ),
    40: ShieldKeyData(
        area_name="Celestial Archives",
        room_name="Synergy Core",
        entity_id=56,
        unlock_message=UnlockMessage.SHIELD,
    ),
    41: ShieldKeyData(
        area_name="Celestial Archives",
        room_name="Docking Bay",
        entity_id=14,
        unlock_message=UnlockMessage.SHIELD,
    ),
    42: ShieldKeyData(
        area_name="Celestial Archives",
        room_name="Incubation Vault 01",
        entity_id=29,
        unlock_message=UnlockMessage.SHIELD,
    ),
    43: ShieldKeyData(
        area_name="Celestial Archives",
        room_name="New Arrival Registration",
        entity_id=49,
        unlock_message=UnlockMessage.SHIELD,
    ),
    44: ShieldKeyData(
        area_name="Vesper Defense Outpost",
        room_name="Compression Chamber",
        entity_id=35,
        unlock_message=UnlockMessage.FORCE_FIELD,
    ),
    45: ShieldKeyData(
        area_name="Vesper Defense Outpost",
        room_name="Weapons Complex",
        entity_id=38,
        unlock_message=UnlockMessage.FORCE_FIELD,
    ),
    46: ShieldKeyData(
        area_name="Vesper Defense Outpost",
        room_name="Weapons Complex",
        entity_id=60,
        unlock_message=UnlockMessage.SHIELD,
    ),
    47: ShieldKeyData(
        area_name="Vesper Defense Outpost",
        room_name="Stasis Bunker",
        entity_id=21,
        unlock_message=UnlockMessage.SHIELD,
    ),
    48: ShieldKeyData(
        area_name="Vesper Defense Outpost",
        room_name="Stasis Bunker",
        entity_id=79,
        unlock_message=UnlockMessage.SHIELD,
    ),
    49: ShieldKeyData(
        area_name="Vesper Defense Outpost",
        room_name="Fuel Stack",
        entity_id=57,
        unlock_message=UnlockMessage.SHIELD,
    ),
    50: ShieldKeyData(
        area_name="Arcterra",
        room_name="Sic Transit",
        entity_id=42,
        unlock_message=UnlockMessage.DOOR,
    ),
    51: ShieldKeyData(
        area_name="Arcterra",
        room_name="Ice Hive",
        entity_id=124,
        unlock_message=UnlockMessage.FORCE_FIELD,
    ),
    52: ShieldKeyData(
        area_name="Arcterra",
        room_name="Frost Labyrinth",
        entity_id=31,
        unlock_message=UnlockMessage.DOOR,
    ),
    53: ShieldKeyData(
        area_name="Arcterra",
        room_name="Fault Line",
        entity_id=29,
        unlock_message=UnlockMessage.FORCE_FIELD,
    ),
    54: ShieldKeyData(
        area_name="Arcterra",
        room_name="Sanctorus",
        entity_id=35,
        unlock_message=UnlockMessage.SHIELD,
    ),
    55: ShieldKeyData(
        area_name="Arcterra",
        room_name="Subterranean",
        entity_id=3,
        unlock_message=UnlockMessage.SHIELD,
    ),
}


def get_state_bit(state_bit: int) -> ShieldKeyData:
    return STATE_BIT_SHIELD_KEY_MAPPING[state_bit]


def create_shield_key_messages() -> list[str]:
    pickup_messages = []
    for key_data in STATE_BIT_SHIELD_KEY_MAPPING.values():
        pickup_messages.append(
            "PSHIELD KEY FOUND\\"
            f"{key_data.unlock_message} in {key_data.area_name.upper()} - {key_data.room_name.upper()}!"
        )
    return pickup_messages


def create_shield_key_triggers(file_manager: FileManager) -> None:
    for state_bit, shield_key_data in STATE_BIT_SHIELD_KEY_MAPPING.items():
        # Get the Shield Key
        entity_file = file_manager.get_entity_file(shield_key_data.area_name, shield_key_data.room_name)
        shield_key = entity_file.get_entity(shield_key_data.entity_id, ItemSpawn)

        # Create a new trigger that checks if the state bit is set
        # If set, it sends out the original message of the shield key
        shield_key_trigger = TriggerVolume.create(
            node_name=shield_key.node_name,
            layer_state=shield_key.layer_state,
            subtype=TriggerVolumeType.STATE_BITS,
            volume=SphereVolumeType.create(
                sphere_radius=75.0,
            ),
            required_state_bit=state_bit,
            trigger_flags=TriggerVolumeFlags.PLAYER_BIPED | TriggerVolumeFlags.PLAYER_ALT,
            parent_id=shield_key.notify_entity_id,
            parent_message=shield_key.collected_message,
        )
        entity_file.append_entity(shield_key_trigger)
