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
        _add_game_messages_strings(file_manager, language, ammo_sizes["missile_launcher"])
        _add_scan_log_strings(file_manager, language)


def _patch_hints(file_manager: FileManager, language: Language, hints: dict[str, str]) -> None:
    scan_log = file_manager.get_string_table(language, StringTables.SCAN_LOG)

    for string_id, text in hints.items():
        string_entry = scan_log.get_string(string_id)
        string_entry.text = text


def _patch_ammo(file_manager: FileManager, language: Language, ammo_sizes: dict[str, int]) -> None:
    missiles = ammo_sizes["missile_expansion"]
    ua = ammo_sizes["ua_expansion"]

    game_messages = file_manager.get_string_table(language, StringTables.GAME_MESSAGES)
    scan_log = file_manager.get_string_table(language, StringTables.SCAN_LOG)

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


def _add_game_messages_strings(file_manager: FileManager, language: Language, missile_launcher_ammo: int) -> None:
    game_messages = file_manager.get_string_table(language, StringTables.GAME_MESSAGES)
    template_string = game_messages.get_string("100M")

    custom_game_messages: list = [
        (
            "PMISSILE LAUNCHER FOUND\\you've obtained the MISSILE LAUNCHER. "
            f"your MISSILE capacity is increased by {missile_launcher_ammo} UNITS."
        ),
        "PNOTHING FOUND\\you've obtained NOTHING.",
    ]

    for custom_game_message in custom_game_messages:
        new_string = game_messages.append_string("M", template_string)
        new_string.text = custom_game_message


def _add_scan_log_strings(file_manager: FileManager, language: Language) -> None:
    scan_log = file_manager.get_string_table(language, StringTables.SCAN_LOG)
    template_string = scan_log.get_string("100L")

    custom_scan_logs: list = [
        "NOTHING\\a nothing item.",
    ]
    for custom_scan_log in custom_scan_logs:
        new_string = scan_log.append_string("L", template_string)
        new_string.text = custom_scan_log
