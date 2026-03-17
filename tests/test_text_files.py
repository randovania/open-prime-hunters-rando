import pytest

from open_prime_hunters_rando.parsing.formats.metroidhunters_text import MetroidHuntersTextFile

all_text_files = [
    "metroidhunters_text_de",
    "metroidhunters_text_en",
    "metroidhunters_text_en-gb",
    "metroidhunters_text_es",
    "metroidhunters_text_fr",
    "metroidhunters_text_it",
    # "metroidhunters_text_jp", # FIXME: Does not parse
]


@pytest.fixture(scope="module", params=all_text_files)
def text_file(rom, request):
    return rom.getFileByName(f"frontend/{request.param}.bin")


def test_compare_text_file(text_file):
    parsed = MetroidHuntersTextFile.parse(text_file)
    built = MetroidHuntersTextFile.build(parsed)

    assert parsed == MetroidHuntersTextFile.parse(built)


def test_get_string(text_file):
    parsed = MetroidHuntersTextFile.parse(text_file)
    parsed.get_string(2544).text = "I am the best in the world!"

    built = MetroidHuntersTextFile.build(parsed)

    assert parsed == MetroidHuntersTextFile.parse(built)
