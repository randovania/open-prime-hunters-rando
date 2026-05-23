import dataclasses

from open_prime_hunters_rando.parsing.common_types.volume import TriggerVolumeFlags
from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.parsing.formats.entities.entity_types.item_spawn import ItemSpawn
from open_prime_hunters_rando.parsing.formats.entities.entity_types.trigger_volume import (
    TriggerVolume,
    TriggerVolumeType,
)


@dataclasses.dataclass(frozen=True)
class ShieldKeyData:
    area_name: str
    room_name: str
    entity_id: int


STATE_BIT_SHIELD_KEY_MAPPING: dict[int, ShieldKeyData] = {
    32: ShieldKeyData(
        area_name="Alinos",
        room_name="Echo Hall",
        entity_id=42,
    ),
    33: ShieldKeyData(
        area_name="Alinos",
        room_name="Elder Passage",
        entity_id=29,
    ),
    34: ShieldKeyData(
        area_name="Alinos",
        room_name="High Ground",
        entity_id=81,
    ),
    35: ShieldKeyData(
        area_name="Alinos",
        room_name="Crash Site",
        entity_id=8,
    ),
    36: ShieldKeyData(
        area_name="Alinos",
        room_name="Council Chamber",
        entity_id=61,
    ),
    37: ShieldKeyData(
        area_name="Alinos",
        room_name="Piston Cave",
        entity_id=80,
    ),
    38: ShieldKeyData(
        area_name="Celestial Archives",
        room_name="Data Shrine 01",
        entity_id=46,
    ),
    39: ShieldKeyData(
        area_name="Celestial Archives",
        room_name="Data Shrine 03",
        entity_id=45,
    ),
    40: ShieldKeyData(
        area_name="Celestial Archives",
        room_name="Synergy Core",
        entity_id=56,
    ),
    41: ShieldKeyData(
        area_name="Celestial Archives",
        room_name="Docking Bay",
        entity_id=14,
    ),
    42: ShieldKeyData(
        area_name="Celestial Archives",
        room_name="Incubation Vault 01",
        entity_id=29,
    ),
    43: ShieldKeyData(
        area_name="Celestial Archives",
        room_name="New Arrival Registration",
        entity_id=49,
    ),
    44: ShieldKeyData(
        area_name="Vesper Defense Outpost",
        room_name="Compression Chamber",
        entity_id=35,
    ),
    45: ShieldKeyData(
        area_name="Vesper Defense Outpost",
        room_name="Weapons Complex",
        entity_id=38,
    ),
    46: ShieldKeyData(
        area_name="Vesper Defense Outpost",
        room_name="Weapons Complex",
        entity_id=60,
    ),
    47: ShieldKeyData(
        area_name="Vesper Defense Outpost",
        room_name="Stasis Bunker",
        entity_id=21,
    ),
    48: ShieldKeyData(
        area_name="Vesper Defense Outpost",
        room_name="Stasis Bunker",
        entity_id=79,
    ),
    49: ShieldKeyData(
        area_name="Vesper Defense Outpost",
        room_name="Fuel Stack",
        entity_id=57,
    ),
    50: ShieldKeyData(
        area_name="Arcterra",
        room_name="Sic Transit",
        entity_id=42,
    ),
    51: ShieldKeyData(
        area_name="Arcterra",
        room_name="Ice Hive",
        entity_id=124,
    ),
    52: ShieldKeyData(
        area_name="Arcterra",
        room_name="Frost Labyrinth",
        entity_id=31,
    ),
    53: ShieldKeyData(
        area_name="Arcterra",
        room_name="Fault Line",
        entity_id=29,
    ),
    54: ShieldKeyData(
        area_name="Arcterra",
        room_name="Sanctorus",
        entity_id=35,
    ),
    55: ShieldKeyData(
        area_name="Arcterra",
        room_name="Subterranean",
        entity_id=3,
    ),
}


def _get_state_bit(state_bit: int) -> ShieldKeyData:
    return STATE_BIT_SHIELD_KEY_MAPPING[state_bit]


def add_shield_key_triggers(file_manager: FileManager) -> None:
    for state_bit in STATE_BIT_SHIELD_KEY_MAPPING.keys():
        # Get the Shield Key
        key_data = _get_state_bit(state_bit)
        entity_file = file_manager.get_entity_file(key_data.area_name, key_data.room_name)
        shield_key = entity_file.get_entity(key_data.entity_id, ItemSpawn)

        # Create a new trigger that checks if the state bit is set
        # If set, it sends out the original message of the shield key
        shield_key_trigger = TriggerVolume.create(
            node_name=shield_key.node_name,
            layer_state=shield_key.layer_state,
            subtype=TriggerVolumeType.STATE_BITS,
            required_state_bit=state_bit,
            trigger_flags=TriggerVolumeFlags.PLAYER_BIPED | TriggerVolumeFlags.PLAYER_ALT,
            parent_id=shield_key.notify_entity_id,
            parent_message=shield_key.collected_message,
        )
        entity_file.append_entity(shield_key_trigger)
