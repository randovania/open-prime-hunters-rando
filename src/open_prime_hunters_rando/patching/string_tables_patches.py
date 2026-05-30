from enum import Enum

from open_prime_hunters_rando.parsing.file_manager import FileManager, Language
from open_prime_hunters_rando.parsing.formats.string_tables import ScanCategory, ScanSpeed


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
        _patch_hints(file_manager, language, string_tables.get("scan_log", {}))
        _patch_ammo(file_manager, language, ammo_sizes)
        _patch_alimbic_cannon_control_room(file_manager, language, configuration["starting_items"]["octoliths"])
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


def _patch_alimbic_cannon_control_room(file_manager: FileManager, language: Language, starting_octoliths: str) -> None:
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

    game_messages = file_manager.get_string_table(language, StringTables.GAME_MESSAGES)

    required_octoliths_message = game_messages.get_string("440M")
    required_octoliths_message.text = required_octoliths_message.text.replace(
        "EIGHT OCTOLITHS", octolith_mapping[required_octoliths]
    )


def _add_game_messages_strings(file_manager: FileManager, language: Language, missile_launcher_ammo: int) -> None:
    game_messages = file_manager.get_string_table(language, StringTables.GAME_MESSAGES)

    custom_game_messages: list = [
        (
            "PMISSILE LAUNCHER FOUND\\you've obtained the MISSILE LAUNCHER. "
            f"your MISSILE capacity is increased by {missile_launcher_ammo} UNITS."
        ),
        "PNOTHING FOUND\\you've obtained NOTHING.",
    ]

    for custom_game_message in custom_game_messages:
        new_string = game_messages.append_string("M")
        new_string.text = custom_game_message


def _add_scan_log_strings(file_manager: FileManager, language: Language) -> None:
    scan_log = file_manager.get_string_table(language, StringTables.SCAN_LOG)

    custom_scan_logs: list = [
        {
            "text": "NOTHING\\a nothing item.",
            "scan_speed": ScanSpeed.FAST,
            "scan_category": ScanCategory.EQUIPMENT,
        },
    ]

    for custom_scan_log in custom_scan_logs:
        new_string = scan_log.append_string("L")
        new_string.text = custom_scan_log["text"]
        new_string.scan_speed = custom_scan_log["scan_speed"]
        new_string.scan_category = custom_scan_log["scan_category"]
