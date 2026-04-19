from enum import Enum

from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.parsing.formats.metroidhunters_text import MetroidHuntersTextFile
from open_prime_hunters_rando.patching.version_checking import Revision, RomData


class MetroidHuntersTextFiles(Enum):
    ENGLISH = "metroidhunters_text_en"
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
        # ENGLISH_GB does not exist on Rev0
        if language == MetroidHuntersTextFiles.ENGLISH_GB and RomData.version == Revision.REV0:
            continue
        _add_patcher_version(file_manager, language.value, text_patches)


def _add_patcher_version(file_manager: FileManager, text_file: MetroidHuntersTextFile, text_patches: dict) -> None:
    patcher_version = text_patches.get("patcher_version", "development version")
    if patcher_version != "development version":
        patcher_version = f"v{patcher_version}"

    menu_text = f"Open Prime Hunters Randomizer\n{patcher_version}"
    file_select_screen = file_manager.get_metroidhunters_text_file(text_file)
    data_offset = 7944 if RomData.version == Revision.REV0 else 6792
    file_select_screen.get_string(data_offset).text = menu_text
