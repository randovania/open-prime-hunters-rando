import json
import logging
import typing
from pathlib import Path

import jsonschema
from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.pickup import patch_pickups

T = typing.TypeVar("T")
LOG = logging.getLogger("prime_hunters_patcher")


def _read_schema() -> dict:
    with Path(__file__).parent.joinpath("files", "schema.json").open() as f:
        return json.load(f)


def patch_rom(input_path: Path, output_path: Path, configuration: dict) -> None:
    LOG.info("Will patch files at %s", input_path)

    jsonschema.validate(instance=configuration, schema=_read_schema())

    # Load rom file as input
    rom = NintendoDSRom.fromFile(input_path)

    # Patch pickups
    patch_pickups(rom, configuration["areas"])

    # Save changes to a new rom
    rom.saveToFile(output_path)

    logging.info("Done")
