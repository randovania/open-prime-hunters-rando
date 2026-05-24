import json
import typing
from pathlib import Path

from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.logger import LOG
from open_prime_hunters_rando.parsing.file_manager import FileManager
from open_prime_hunters_rando.patching import game_version
from open_prime_hunters_rando.patching.asm.arm9 import patch_arm9
from open_prime_hunters_rando.patching.asm.overlays import patch_overlays
from open_prime_hunters_rando.patching.entities.entity_patching import patch_entities
from open_prime_hunters_rando.patching.escape_sequence_patches import patch_escape_sequences
from open_prime_hunters_rando.patching.hunter_spawn_patches import patch_hunters
from open_prime_hunters_rando.patching.state_bits import add_shield_key_triggers
from open_prime_hunters_rando.patching.static_patches import static_patches
from open_prime_hunters_rando.patching.string_tables_patches import patch_string_tables
from open_prime_hunters_rando.patching.text_patches import patch_text_files
from open_prime_hunters_rando.validator_with_default import DefaultValidatingDraft7Validator

T = typing.TypeVar("T")


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

    # Get the version data for the rom
    version = game_version.get_version(rom, game_version.ALL_VERSIONS)

    # Initialize the file manager
    file_manager = FileManager(rom, export_parsed_files)

    # Modify main code file arm9.bin
    LOG.info("Patching arm9.bin")
    patch_arm9(rom, version, configuration)

    # Modify overlay files
    LOG.info("Patching overlays")
    patch_overlays(rom, version)

    # Static patches to rooms
    LOG.info("Patching rooms")
    static_patches(file_manager)

    # Patch escape sequences
    LOG.info("Removing escape sequences")
    patch_escape_sequences(file_manager)

    # Patch shield keys
    LOG.info("Patching shield keys")
    add_shield_key_triggers(file_manager)

    # Patch entities
    patch_entities(file_manager, configuration["areas"])

    # Patch Hunter Spawns
    patch_hunters(file_manager, configuration)

    # Patch string tables
    LOG.info("Patching string tables")
    patch_string_tables(file_manager, configuration)

    # Patch frontend text files
    LOG.info("Patching frontend text files")
    patch_text_files(version, file_manager, configuration.get("text_patches", {}))

    # Save all changes to a new rom
    file_manager.save_to_rom(output_path)

    LOG.info("Done")
