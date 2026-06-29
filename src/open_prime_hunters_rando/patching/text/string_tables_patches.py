from enum import Enum
from typing import TypedDict

from open_prime_hunters_rando.parsing.file_manager import FileManager, Language
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_file import EntityFile
from open_prime_hunters_rando.parsing.formats.entities.entity_types.artifact import Artifact, ModelId
from open_prime_hunters_rando.parsing.formats.entities.entity_types.item_spawn import ItemSpawn
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType, ItemType
from open_prime_hunters_rando.parsing.formats.string_tables import ScanCategory, ScanSpeed, StringTable
from open_prime_hunters_rando.parsing.level_data import ALL_AREAS
from open_prime_hunters_rando.patching.entities.state_bits import create_shield_key_messages


class StringTables(Enum):
    GAME_MESSAGES = "GameMessages"
    HUD_MESSAGES_MP = "HudMessagesMP"
    HUD_MESSAGES_SP = "HudMessagesSP"
    HUD_MSGS_COMMON = "HudMsgsCommon"
    LOCATION_NAMES = "LocationNames"
    MB_BANNER = "MBBanner"
    SCAN_LOG = "ScanLog"
    SHIP_IN_SPACE = "ShipInSpace"
    SHIP_ON_GROUND = "ShipOnGround"
    WEAPON_NAMES = "WeaponNames"


class RefillProperties(TypedDict):
    original_value: int
    new_value: int
    string_ids: list[str]


type StringTablesConfig = dict[str, dict[str, str]]


def patch_string_tables(file_manager: FileManager, configuration: dict) -> None:
    ammo_sizes: dict[str, int] = configuration.get("ammo_sizes", {})
    refill_sizes: dict[str, int] = configuration.get("refill_sizes", {})
    string_tables: StringTablesConfig = configuration["text_patches"]["string_tables"]

    for language in Language:
        scan_log = file_manager.get_string_table(language, StringTables.SCAN_LOG)
        game_messages = file_manager.get_string_table(language, StringTables.GAME_MESSAGES)
        hud_messages_sp = file_manager.get_string_table(language, StringTables.HUD_MESSAGES_SP)
        ship_in_space = file_manager.get_string_table(language, StringTables.SHIP_IN_SPACE)

        _patch_string_table_configs(string_tables, scan_log, ship_in_space)
        _patch_ammo(scan_log, game_messages, ammo_sizes)
        _patch_refills(scan_log, refill_sizes)
        _patch_alimbic_cannon_control_room(game_messages, configuration["starting_items"]["octoliths"])
        _add_game_messages_strings(game_messages)
        _add_scan_log_strings(scan_log)
        _add_hud_messages_strings(hud_messages_sp, ammo_sizes["missile_launcher"])
        _patch_elder_passage_scan(scan_log, file_manager.get_entity_file("Alinos", "Elder Passage"))


def _patch_string_table_configs(
    string_tables: StringTablesConfig, scan_log: StringTable, ship_in_space: StringTable
) -> None:
    string_tables_mapping: list[tuple[StringTable, dict[str, str]]] = [
        (scan_log, string_tables.get("scan_log", {})),  # Hints
        (ship_in_space, string_tables.get("ship_in_space", {})),  # Intro Text
    ]
    for string_table, config in string_tables_mapping:
        for string_id, text in config.items():
            string_entry = string_table.get_string(string_id)
            string_entry.text = text


def _patch_ammo(scan_log: StringTable, game_messages: StringTable, ammo_sizes: dict[str, int]) -> None:
    missiles = ammo_sizes["missile_expansion"]
    ua = ammo_sizes["ua_expansion"]

    # Missile Expansion
    if missiles != 10:
        missile_pickup_string = game_messages.get_string("300M")
        missile_pickup_string.text = missile_pickup_string.text.replace("10", f"{missiles}")

        missile_scan_string = scan_log.get_string("310L")
        missile_scan_string.text = missile_scan_string.text.replace("10", f"{missiles}")

    # UA Expansion
    if ua != 30:
        ammo_pickup_string = game_messages.get_string("640M")
        ammo_pickup_string.text = ammo_pickup_string.text.replace("30", f"{ua}")

        ammo_scan_string = scan_log.get_string("420L")
        ammo_scan_string.text = ammo_scan_string.text.replace("30", f"{ua}")


def _patch_refills(scan_log: StringTable, refill_sizes: dict[str, int]) -> None:
    refill_mapping: dict[str, RefillProperties] = {
        "small_energy": {
            "original_value": 30,
            "new_value": refill_sizes["small_energy"],
            "string_ids": ["900L"],
        },
        "medium_energy": {
            "original_value": 60,
            "new_value": refill_sizes["medium_energy"],
            "string_ids": ["110L"],
        },
        "large_energy": {
            "original_value": 100,
            "new_value": refill_sizes["large_energy"],
            "string_ids": ["210L"],
        },
        "small_ammo": {
            "original_value": 10,
            "new_value": refill_sizes["small_ammo"],
            "string_ids": ["410L", "610L"],
        },
        "large_ammo": {
            "original_value": 25,
            "new_value": refill_sizes["large_ammo"],
            "string_ids": ["510L", "710L"],
        },
    }

    for refill_type, properties in refill_mapping.items():
        if properties["original_value"] != properties["new_value"]:
            for string_id in properties["string_ids"]:
                refill_string = scan_log.get_string(string_id)
                refill_string.text = refill_string.text.replace(
                    str(properties["original_value"]), str(properties["new_value"])
                )


def _patch_alimbic_cannon_control_room(game_messages: StringTable, starting_octoliths: str) -> None:
    required_octoliths = starting_octoliths.count("0")
    if required_octoliths in [0, 8]:
        return

    octolith_mapping: dict[int, str] = {
        1: "ONE OCTOLITH",
        2: "TWO OCTOLITHS",
        3: "THREE OCTOLITHS",
        4: "FOUR OCTOLITHS",
        5: "FIVE OCTOLITHS",
        6: "SIX OCTOLITHS",
        7: "SEVEN OCTOLITHS",
    }

    required_octoliths_message = game_messages.get_string("440M")
    required_octoliths_message.text = required_octoliths_message.text.replace(
        "EIGHT OCTOLITHS", octolith_mapping[required_octoliths]
    )


def _add_game_messages_strings(game_messages: StringTable) -> None:
    custom_game_messages: list = [
        "PNOTHING FOUND\\you've obtained NOTHING.",
        *create_shield_key_messages(),  # Shield Key Messages
        "AOUBLIETTE\\oubliette",
    ]

    for custom_game_message in custom_game_messages:
        new_string = game_messages.add_string("M")
        new_string.text = custom_game_message


def _add_scan_log_strings(scan_log: StringTable) -> None:
    custom_scan_logs: list = [
        {
            "text": "NOTHING\\a nothing item.",
            "scan_speed": ScanSpeed.FAST,
            "scan_category": ScanCategory.EQUIPMENT,
        },
        *_create_portal_destination_scans(),  # Custom portal scans are added in order of room id
    ]

    for custom_scan_log in custom_scan_logs:
        new_string = scan_log.add_string("L")
        new_string.text = custom_scan_log["text"]
        new_string.scan_speed = custom_scan_log["scan_speed"]
        new_string.scan_category = custom_scan_log["scan_category"]


def _add_hud_messages_strings(hud_messages_sp: StringTable, missile_launcher_ammo: int) -> None:
    custom_hud_messages: list[str] = [
        f"your $MISSILE$ capacity is increased by {missile_launcher_ammo} UNITS.",
    ]

    for custom_hud_message in custom_hud_messages:
        new_string = hud_messages_sp.add_string("H")
        new_string.text = custom_hud_message


def _create_portal_destination_scans() -> list:
    all_destination_scans = []
    for area_data in ALL_AREAS:
        for room_name, level_data in area_data.items():
            all_destination_scans.append(
                {
                    "text": (
                        "PORTAL DESTINATION\\the destination of this PORTAL is "
                        f"{level_data.area_name.upper()} - {room_name.upper()}."
                    ),
                    "scan_speed": ScanSpeed.FAST,
                    "scan_category": ScanCategory.OBJECT,
                }
            )

    return all_destination_scans


def _patch_elder_passage_scan(scan_log: StringTable, elder_passage: EntityFile) -> None:
    # Change the scan that spawns the Shield Key to mention the item that spawns instead
    item_type_mapping: dict[ItemType, str] = {
        ItemType.HEALTH_SMALL: "SMALL ENERGY",
        ItemType.HEALTH_MEDIUM: "MEDIUM ENERGY",
        ItemType.HEALTH_BIG: "BIG ENERGY",
        ItemType.ENERGY_TANK: "ENERGY TANK",
        ItemType.VOLT_DRIVER: "VOLT DRIVER",
        ItemType.MISSILE_EXPANSION: "MISSILE EXPANSION",
        ItemType.BATTLEHAMMER: "BATTLEHAMMER",
        ItemType.IMPERIALIST: "IMPERIALIST",
        ItemType.JUDICATOR: "JUDICATOR",
        ItemType.MAGMAUL: "MAGMAUL",
        ItemType.SHOCK_COIL: "SHOCK COIL",
        ItemType.OMEGA_CANNON: "OMEGA CANNON",
        ItemType.UA_SMALL: "SMALL UA PACK",
        ItemType.UA_BIG: "LARGE UA PACK",
        ItemType.MISSILE_SMALL: "SMALL MISSILE PACK",
        ItemType.MISSILE_BIG: "LARGE MISSILE PACK",
        ItemType.CLOAK: "NOTHING",
        ItemType.UA_EXPANSION: "UA EXPANSION",
        ItemType.ARTIFACT_KEY: "SHIELD KEY",
        ItemType.AFFINITY_WEAPON: "MISSILE LAUNCHER",
    }

    shield_key = elder_passage.get_entity(29, Entity)
    if shield_key.entity_type == EntityType.ITEM_SPAWN:
        assert isinstance(shield_key, ItemSpawn)
        new_name = item_type_mapping[shield_key.item_type]
    else:
        assert isinstance(shield_key, Artifact)
        if shield_key.model_id == ModelId.OCTOLITH:
            new_name = "OCTOLITH"
        else:
            new_name = "ARTIFACT"

    string = scan_log.get_string("164L")
    string.text = string.text.replace("SHIELD KEY", new_name)
