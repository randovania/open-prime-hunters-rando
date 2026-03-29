from enum import Enum

from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.parsing.formats.metroidhunters_text import MetroidHuntersTextFile


class MetroidHuntersTextFiles(Enum):
    ENGLISH_US = "metroidhunters_text_en"
    ENGLISH_GB = "metroidhunters_text_en-gb"
    FRENCH = "metroidhunters_text_fr"
    GERMAN = "metroidhunters_text_de"
    ITALIAN = "metroidhunters_text_it"
    JAPANESE = "metroidhunters_text_jp"
    SPANISH = "metroidhunters_text_es"


def patch_text_files(file_manager: FileManager, text_patches: dict) -> None:
    for language in MetroidHuntersTextFiles:
        # FIXME: Japanese has parsing issues
        if language == MetroidHuntersTextFiles.JAPANESE:
            continue

        _add_patcher_version(file_manager, language.value)


def _add_patcher_version(file_manager: FileManager, text_file: MetroidHuntersTextFile) -> None:
    patcher_version = "Open Prime Hunters Randomizer\nv" + text_patches.get("patcher_version", "Development Version")
    file_select_screen = file_manager.get_metroidhunters_text_file(text_file)
    file_select_screen.get_string(6792).text = patcher_version
