from pathlib import Path

from construct import Construct, Container, ListContainer
from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.entities.entity_type import EntityFile
from open_prime_hunters_rando.entities.force_field import patch_force_fields
from open_prime_hunters_rando.entities.pickup import patch_pickups
from open_prime_hunters_rando.level_data import LevelData, get_data


def patch_entities(rom: NintendoDSRom, configuration: dict[str, dict]) -> None:
    for area_name, area_config in configuration.items():
        for level_name, level_config in area_config.items():
            for room_name, entity_groups in level_config.items():
                # Load the entity file for the room
                level_data = get_data(area_name, room_name)
                file_name = f"levels/entities/{level_data.entity_file}.bin"

                # Parse the file into a construct
                parsed_file = EntityFile.parse(rom.getFileByName(file_name))

                # Modify entities
                patch_pickups(parsed_file, entity_groups["pickups"])
                patch_force_fields(parsed_file, entity_groups["force_fields"])

                # Overwrite the file with the modified parsed data
                rom.setFileByName(file_name, EntityFile.build(parsed_file))

                # # Uncomment to export all parsed entity files
                # _export_parsed_entity_files(level_data, parsed_file)


def _export_parsed_entity_files(level_data: LevelData, parsed_file: Construct) -> None:
    to_export = Container(
        {
            "header": parsed_file._raw.header,
            "entities": ListContainer([e._raw for e in parsed_file.entities]),
        }
    )

    export_path = Path(__file__).parent.joinpath("parsed_files")
    export_path.mkdir(parents=True, exist_ok=True)
    with Path.open(export_path / f"{level_data.entity_file}.txt", "w") as f:
        f.write(str(to_export))
