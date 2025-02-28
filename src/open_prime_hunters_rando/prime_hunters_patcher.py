import json
import logging
import typing
from pathlib import Path

import jsonschema

T = typing.TypeVar("T")
LOG = logging.getLogger("prime_hunters_patcher")


def _read_schema():
    with Path(__file__).parent.joinpath("schema.json").open() as f:
        return json.load(f)


def patch(input_path: Path, output_path: Path, configuration: dict):
    LOG.info("Will patch files at %s", input_path)

    jsonschema.validate(instance=configuration, schema=_read_schema())

    logging.info("Done")
