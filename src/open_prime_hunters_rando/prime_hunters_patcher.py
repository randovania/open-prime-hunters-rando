import json
import logging
import ndspy.rom
import typing
from pathlib import Path

import jsonschema

T = typing.TypeVar("T")
LOG = logging.getLogger("prime_hunters_patcher")


def _read_schema():
    with Path(__file__).parent.joinpath("files", "schema.json").open() as f:
        return json.load(f)


def patch(input_path: Path, output_path: Path, configuration: dict):
    LOG.info("Will patch files at %s", input_path)

    jsonschema.validate(instance=configuration, schema=_read_schema())

    # Load rom file as input
    rom = ndspy.rom.NintendoDSRom.fromFile(input_path)

    # Save changes to a new rom
    rom.saveToFile(output_path)

    logging.info("Done")
