import json
import logging
import typing
from pathlib import Path

import jsonschema
import ndspy.rom

T = typing.TypeVar("T")
LOG = logging.getLogger("prime_hunters_patcher")


def _read_schema():
    with Path(__file__).parent.joinpath("files", "schema.json").open() as f:
        return json.load(f)


def patch_pickups(rom: ndspy.rom.NintendoDSRom, configuration: dict[str, dict]):
    for area_name, area_config in configuration.items():
        for level_name, level_config in area_config.items():
            for room_name, room_config in level_config.items():
                entity_file = room_config["entity_file"]
                file_path = f"levels/entities/{entity_file}.bin"
                file = rom.getFileByName(file_path)
                for pickup in room_config["pickups"]:
                    offset = int(pickup["offset"], 16)
                    item_type = pickup["item_type"]
                    file[offset : offset + 1] = item_type.to_bytes(1, "big")


def patch_rom(input_path: Path, output_path: Path, configuration: dict):
    LOG.info("Will patch files at %s", input_path)

    jsonschema.validate(instance=configuration, schema=_read_schema())

    # Load rom file as input
    rom = ndspy.rom.NintendoDSRom.fromFile(input_path)

    # Patch pickups
    patch_pickups(rom, configuration["areas"])

    # Save changes to a new rom
    rom.saveToFile(output_path)

    logging.info("Done")
