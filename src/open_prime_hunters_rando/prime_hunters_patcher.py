import json
import logging
import typing
from pathlib import Path

from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.arm9 import patch_arm9
from open_prime_hunters_rando.entities.entity_patching import patch_entities
from open_prime_hunters_rando.static_patches import static_patches
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


def patch_rom(input_path: Path, output_path: Path, configuration: dict) -> None:
    LOG.info("Will patch files at %s", input_path)

    validate(configuration)

    # Load rom file as input
    rom = DebugNintendoDsRom.fromFile(input_path)

    # Modify main code file arm9.bin
    patch_arm9(rom, configuration["starting_items"])

    # Static patches to rooms
    static_patches(rom)

    # Patch entities
    patch_entities(rom, configuration["areas"])

    # Save changes to a new rom
    rom.saveToFile(output_path)

    logging.info("Done")
