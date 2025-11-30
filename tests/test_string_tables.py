import pytest

from open_prime_hunters_rando.file_manager import StringTables
from open_prime_hunters_rando.string_tables.string_tables import StringTable

all_string_tables = [
    StringTables.GAME_MESSAGES.value,
    StringTables.HUD_MESSAGES_MP.value,
    StringTables.HUD_MESSAGES_SP.value,
    StringTables.HUD_MSGS_COMMON.value,
    StringTables.LOCATION_NAMES.value,
    StringTables.MB_BANNER.value,
    StringTables.SCAN_LOG.value,
    StringTables.SHIP_IN_SPACE.value,
    StringTables.SHIP_ON_GROUND.value,
    StringTables.WEAPON_NAMES.value,
]


@pytest.fixture(scope="module", params=all_string_tables)
def string_table(rom, request):
    return rom.getFileByName(f"stringTables/{request.param}.bin")


def test_compare_string_table(string_table):
    parsed = StringTable.parse(string_table)
    built = StringTable.build(parsed)

    assert string_table == built
    assert parsed == StringTable.parse(built)
