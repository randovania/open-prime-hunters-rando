from enum import Enum

from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.parsing.formats.metroidhunters_text import MetroidHuntersTextFile
from open_prime_hunters_rando.patching.version_checking import IdCode, Revision, RomData


class MetroidHuntersTextFiles(Enum):
    ENGLISH = "metroidhunters_text_en"
    ENGLISH_GB = "metroidhunters_text_en-gb"
    FRENCH = "metroidhunters_text_fr"
    GERMAN = "metroidhunters_text_de"
    ITALIAN = "metroidhunters_text_it"
    # JAPANESE = "metroidhunters_text_jp"
    SPANISH = "metroidhunters_text_es"


def patch_text_files(file_manager: FileManager, text_patches: dict) -> None:
    rom_data = RomData(file_manager.rom)
    for language_file in MetroidHuntersTextFiles:
        # ENGLISH_GB does not exist on US Rev0
        if (
            language_file == MetroidHuntersTextFiles.ENGLISH_GB
            and rom_data.id_code == IdCode.AMHE
            and rom_data.version == Revision.REV0
        ):
            continue

        text_file = file_manager.get_metroidhunters_text_file(language_file)

        _add_patcher_version(rom_data, text_file, text_patches)


def _add_patcher_version(rom_data: RomData, text_file: MetroidHuntersTextFile, text_patches: dict) -> None:
    patcher_version = text_patches.get("patcher_version", "Open Prime Hunters Rando\ndevelopment version")
    data_offset = 7944 if rom_data.version == Revision.REV0 else 6792
    text_file.get_string(data_offset).text = patcher_version
