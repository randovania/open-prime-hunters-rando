from pathlib import Path

from construct import Container, ListContainer
from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.entities.entity_type import EntityFile
from open_prime_hunters_rando.level_data import get_data


class FileManager:
    def __init__(self, rom: NintendoDSRom):
        self.rom = rom
        self.entity_files: dict[str, EntityFile] = {}

    def get_entity_file(self, area_name: str, room_name: str) -> EntityFile:
        level_data = get_data(area_name, room_name)
        file_name = f"levels/entities/{level_data.entity_file}.bin"
        if file_name not in self.entity_files:
            self.entity_files[file_name] = EntityFile.parse(self.rom.getFileByName(file_name))
        return self.entity_files[file_name]

    def finalize_entity_files(self) -> None:
        for file_name, entity_file in self.entity_files.items():
            self.rom.setFileByName(file_name, entity_file.build())

            # # Uncomment to export parsed entity file
            # self.export_entity_file(file_name, entity_file)

    def export_entity_file(self, file_name: str, entity_file: EntityFile) -> None:
        to_export = Container(
            {
                "header": entity_file._raw.header,
                "entities": ListContainer([e._raw for e in entity_file.entities]),
            }
        )

        export_path = Path(__file__).parent.joinpath("entities", "entity_files")
        export_path.mkdir(parents=True, exist_ok=True)
        with Path.open(export_path / f"{file_name[16:-4]}.txt", "w") as f:
            f.write(str(to_export))
