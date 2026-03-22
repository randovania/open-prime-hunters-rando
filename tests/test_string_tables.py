import pytest

from open_prime_hunters_rando.parsing.construct_extensions import ShortUtf8CString
from open_prime_hunters_rando.parsing.file_manager import Language
from open_prime_hunters_rando.parsing.formats.string_tables import StringTable
from open_prime_hunters_rando.patching.string_tables_patches import StringTables

all_string_tables = [string_table.value for string_table in StringTables]

all_languages = [language.value for language in Language]


@pytest.fixture(scope="module", params=all_languages)
def language(request):
    return request.param


@pytest.fixture(scope="module", params=all_string_tables)
def string_table(rom, request, language):
    return rom.getFileByName(f"{language}/{request.param}.bin")


def test_compare_string_table(string_table):
    parsed = StringTable.parse(string_table)
    built = StringTable.build(parsed)

    assert string_table == built
    assert parsed == StringTable.parse(built)


def test_short_utf8_cstring():
    data = b"TTELEPATHISCHE BOTSCHAFT\\\xc0\xa6die schl\xc3\xbcssel sind allerorten\xc0\xa6"
    text = r"TTELEPATHISCHE BOTSCHAFT\…die schlüssel sind allerorten…"

    bytes_to_str = ShortUtf8CString()._bytes_to_str(data)
    assert bytes_to_str == text

    str_to_bytes = ShortUtf8CString()._str_to_bytes(text)
    assert str_to_bytes == data
