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

    _patch_hints(file_manager, string_tables.get("scan_log", {}))
    _patch_pickups(file_manager, configuration.get("game_patches", {}))


def _patch_hints(file_manager: FileManager, hints: dict[str, str]) -> None:
    scan_log = file_manager.get_string_table(Language.ENGLISH, StringTables.SCAN_LOG)  # TODO: Change other languages

    for string_id, text in hints.items():
        string_entry = scan_log.get_string(string_id)
        string_entry.text = text


def _patch_pickups(file_manager: FileManager, game_patches: dict[str, int]) -> None:
    ammo = game_patches.get("ammo_per_expansion")
    missiles = game_patches.get("missiles_per_expansion")

    # No changes were made, so skip
    if ammo == 30 and missiles == 10:
        return

    game_messages = file_manager.get_string_table(Language.ENGLISH, StringTables.GAME_MESSAGES)
    scan_log = file_manager.get_string_table(Language.ENGLISH, StringTables.SCAN_LOG)

    # UA Expansion
    ammo_pickup_string = game_messages.get_string("640M")
    ammo_pickup_string.text = f"PUA EXPANSION FOUND\\your UNIVERSAL AMMO capacity is increased by {ammo} UNITS."

    ammo_scan_string = scan_log.get_string("420L")
    ammo_scan_string.text = f"UA EXPANSION\\increases the UNIVERSAL AMMO capacity by {ammo} UNITS."

    # Missile Expansion
    missile_pickup_string = game_messages.get_string("300M")
    missile_pickup_string.text = f"PMISSILE EXPANSION FOUND\\your MISSILE capacity is increased by {missiles} UNITS."

    missile_scan_string = scan_log.get_string("310L")
    missile_scan_string.text = (
        f"MISSILE EXPANSION\\increases the capacity of the ARM CANNON's arsenal by {missiles} MISSILES."
    )
