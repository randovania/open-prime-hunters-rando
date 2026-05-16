from enum import Enum

from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.parsing.formats.metroidhunters_text import MetroidHuntersTextFile
from open_prime_hunters_rando.patching import game_version
from open_prime_hunters_rando.patching.game_version import GameVersion, IdCode, Revision


class MetroidHuntersTextFiles(Enum):
    ENGLISH = "metroidhunters_text_en"
    ENGLISH_GB = "metroidhunters_text_en-gb"
    FRENCH = "metroidhunters_text_fr"
    GERMAN = "metroidhunters_text_de"
    ITALIAN = "metroidhunters_text_it"
    # JAPANESE = "metroidhunters_text_jp"
    SPANISH = "metroidhunters_text_es"


def patch_text_files(rom: NintendoDSRom, file_manager: FileManager, text_patches: dict) -> None:
    version = game_version.get_version(rom, game_version.ALL_VERSIONS)
    for language_file in MetroidHuntersTextFiles:
        # ENGLISH_GB does not exist on US Rev0
        if (
            language_file == MetroidHuntersTextFiles.ENGLISH_GB
            and version.id_code == IdCode.AMHE
            and version.revision == Revision.REV0
        ):
            continue

        text_file = file_manager.get_metroidhunters_text_file(language_file)

        _add_patcher_version(version, text_file, text_patches)


def _add_patcher_version(version: GameVersion, text_file: MetroidHuntersTextFile, text_patches: dict) -> None:
    data_offset = version.metroidhunters_text_file_offsets.main_menu_textbox
    patcher_version = text_patches.get("patcher_version", "Open Prime Hunters Rando\ndevelopment version")
    text_file.get_string(data_offset).text = patcher_version
