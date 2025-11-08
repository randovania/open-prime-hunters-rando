from enum import Enum

from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.parsing.formats.metroidhunters_text import MetroidHuntersTextFile


class MetroidHuntersTextFiles(Enum):
    ENGLISH = "metroidhunters_text_en"
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

        _add_patcher_version(file_manager, language.value, text_patches)


def _add_patcher_version(file_manager: FileManager, text_file: MetroidHuntersTextFile, text_patches: dict) -> None:
    patcher_version = text_patches.get("patcher_version", "development version")
    if patcher_version != "development version":
        patcher_version = f"v{patcher_version}"

    menu_text = f"Open Prime Hunters Randomizer\n{patcher_version}"
    file_select_screen = file_manager.get_metroidhunters_text_file(text_file)
    file_select_screen.get_string(7944).text = menu_text
