from enum import Enum

from open_prime_hunters_rando.file_manager import FileManager, Language


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


def patch_string_tables(file_manager: FileManager, configuration: dict) -> None:
    string_tables = configuration.get("string_tables", {})
    ammo_sizes = configuration.get("ammo_sizes", {})

    for language in Language:
        # FIXME: Japanese has parsing issues
        if language == Language.JAPANESE:
            continue

        _patch_hints(file_manager, language, string_tables.get("scan_log", {}))
        _patch_ammo(file_manager, language, ammo_sizes)


def _patch_hints(file_manager: FileManager, language: Language, hints: dict[str, str]) -> None:
    scan_log = file_manager.get_string_table(language, StringTables.SCAN_LOG)

    for string_id, text in hints.items():
        string_entry = scan_log.get_string(string_id)
        string_entry.text = text


def _patch_ammo(file_manager: FileManager, language: Language, ammo_sizes: dict[str, int]) -> None:
    missiles = ammo_sizes["missile_expansion"]
    ua = ammo_sizes["ua_expansion"]

    # No changes were made, so skip
    if missiles == 10 and ua == 30:
        return

    game_messages = file_manager.get_string_table(language, StringTables.GAME_MESSAGES)
    scan_log = file_manager.get_string_table(language, StringTables.SCAN_LOG)

    # Missile Expansion
    missile_pickup_string = game_messages.get_string("300M")
    missile_pickup_string.text = missile_pickup_string.text.replace("10", f"{missiles}")

    missile_scan_string = scan_log.get_string("310L")
    missile_scan_string.text = missile_scan_string.text.replace("10", f"{missiles}")

    # UA Expansion
    ammo_pickup_string = game_messages.get_string("640M")
    ammo_pickup_string.text = ammo_pickup_string.text.replace("30", f"{ua}")

    ammo_scan_string = scan_log.get_string("420L")
    ammo_scan_string.text = ammo_scan_string.text.replace("30", f"{ua}")
