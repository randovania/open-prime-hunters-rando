from enum import Enum

from open_prime_hunters_rando.parsing.file_manager import FileManager


class MetroidHuntersTextFiles(Enum):
    ENGLISH_US = "metroidhunters_text_en"
    ENGLISH_GB = "metroidhunters_text_en-gb"
    FRENCH = "metroidhunters_text_fr"
    GERMAN = "metroidhunters_text_de"
    ITALIAN = "metroidhunters_text_it"
    JAPANESE = "metroidhunters_text_jp"
    SPANISH = "metroidhunters_text_es"


def patch_text_files(file_manager: FileManager, configuration: dict) -> None:
    for language in MetroidHuntersTextFiles:
        # FIXME: Japanese has parsing issues
        if language == MetroidHuntersTextFiles.JAPANESE:
            continue

        file_select_screen = file_manager.get_metroidhunters_text_file(language.value)
        file_select_screen.get_string(6792).text = configuration["text_patches"]["patcher_version"]
