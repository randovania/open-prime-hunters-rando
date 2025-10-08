from enum import Enum

from open_prime_hunters_rando.file_manager import FileManager, Language


class StringTable(Enum):
    GAME_MESSAGES = "GameMessages"
    HUD_MESSAGES_MP = "HUDMessagesMP"
    HUD_MESSAGES_SP = "HUDMessagesSP"
    HUD_MSGS_COMMON = "HUDMsgsCommon"
    LOCATION_NAMES = "LocationNames"
    MB_BANNER = "MBBanner"
    SCAN_LOG = "ScanLog"
    SHIP_IN_SPACE = "ShipInSpace"
    SHIP_ON_GROUND = "ShipOnGround"
    WEAPON_NAMES = "WeaponNames"


def patch_string_tables(file_manager: FileManager, string_tables: dict) -> None:
    _patch_hints(file_manager, string_tables.get("scan_log", {}))


def _patch_hints(file_manager: FileManager, hints: dict[str, str]) -> None:
    scan_log = file_manager.get_string_table(Language.ENGLISH, StringTable.SCAN_LOG)  # TODO: Change other languages

    for string_id, text in hints.items():
        string_entry = scan_log.get_string(string_id)
        string_entry.text = text
