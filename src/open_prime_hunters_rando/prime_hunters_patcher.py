import json
import logging
import typing
from pathlib import Path

from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.add_entities import add_new_entities
from open_prime_hunters_rando.arm9 import patch_arm9
from open_prime_hunters_rando.entities.entity_patching import patch_entities
from open_prime_hunters_rando.escape_sequence_patches import patch_escape_sequences
from open_prime_hunters_rando.file_manager import FileManager
from open_prime_hunters_rando.hunter_spawn_patches import patch_hunters
from open_prime_hunters_rando.static_patches import static_patches
from open_prime_hunters_rando.string_tables.string_tables_patches import patch_string_tables
from open_prime_hunters_rando.validator_with_default import DefaultValidatingDraft7Validator

T = typing.TypeVar("T")
LOG = logging.getLogger("prime_hunters_patcher")


class DebugNintendoDsRom(NintendoDSRom):
    def __repr__(self) -> str:
        return f"NintendoDsRom({self.name!r})"


def _read_schema() -> dict:
    with Path(__file__).parent.joinpath("files", "schema.json").open() as f:
        return json.load(f)


def validate(configuration: dict) -> None:
    # validate patcher json with the schema.json
    DefaultValidatingDraft7Validator(_read_schema()).validate(configuration)


def patch_rom(input_path: Path, output_path: Path, configuration: dict, export_parsed_files: bool) -> None:
    LOG.info("Will patch files at %s", input_path)

    validate(configuration)

    # Load rom file as input
    rom = DebugNintendoDsRom.fromFile(input_path)

    # Initialize the file manager
    file_manager = FileManager(rom, export_parsed_files)

    # Modify main code file arm9.bin
    patch_arm9(rom, configuration)

    # Static patches to rooms
    static_patches(file_manager)

    # Patch escape sequences
    patch_escape_sequences(file_manager)

    # Patch entities
    patch_entities(file_manager, configuration["areas"])

    # Add new entities
    add_new_entities(file_manager)

    # Patch Hunter Spawns
    patch_hunters(file_manager, configuration)

    # Patch string tables
    patch_string_tables(file_manager, configuration["string_tables"])

    # Remove later!
    file_manager.get_metroidhunters_text_file("metroidhunters_text_en")

    # Save all changes to a new rom
    file_manager.save_to_rom(output_path)

    logging.info("Done")
