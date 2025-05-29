import logging
from enum import Enum
from pathlib import Path

import construct
from construct import Container, ListContainer
from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.entities.entity_type import EntityFile
from open_prime_hunters_rando.level_data import get_data
from open_prime_hunters_rando.string_tables.string_tables import StringTable


class Language(Enum):
    ENGLISH = "stringTables"
    FRENCH = "stringTables_fr"
    GERMAN = "stringTables_gr"
    ITALIAN = "stringTables_it"
    JAPANESE = "stringTables_jp"
    SPANISH = "stringTables_sp"


class FileManager:
    def __init__(self, rom: NintendoDSRom, export_parsed_files: bool):
        self.rom = rom
        self.entity_files: dict[str, EntityFile] = {}
        self.export_parsed_files = export_parsed_files
        self.string_tables: dict[str, StringTable] = {}
        construct.lib.setGlobalPrintFullStrings(True)

    def get_entity_file(self, area_name: str, room_name: str) -> EntityFile:
        level_data = get_data(area_name, room_name)
        file_name = f"levels/entities/{level_data.entity_file}.bin"
        if file_name not in self.entity_files:
            self.entity_files[file_name] = EntityFile.parse(self.rom.getFileByName(file_name))
        return self.entity_files[file_name]

    def finalize_entity_files(self) -> None:
        for file_name, entity_file in self.entity_files.items():
            self.rom.setFileByName(file_name, entity_file.build())

            # Export parsed entity file
            if self.export_parsed_files:
                self.export_entity_file(file_name, entity_file)

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

    def get_string_table(self, language: Language, string_table: str) -> StringTable:
        file_name = f"{language.value}/{string_table}.bin"
        if file_name not in self.string_tables:
            self.string_tables[file_name] = StringTable.parse(self.rom.getFileByName(file_name))
        return self.string_tables[file_name]

    def finalize_string_tables(self) -> None:
        for file_name, string_table in self.string_tables.items():
            self.rom.setFileByName(file_name, string_table.build())

            # # Uncomment to export parsed string table
            # self.export_string_table(file_name, string_table)

    def export_string_table(self, file_name: str, string_table: StringTable) -> None:
        to_export = Container(
            {
                "header": string_table._raw.header,
                "strings": ListContainer([e._raw for e in string_table.strings]),
            }
        )

        export_path = Path(__file__).parent.joinpath("string_tables")
        export_path.mkdir(parents=True, exist_ok=True)
        with Path.open(export_path / f"{file_name[13:-4]}.txt", "w") as f:
            f.write(str(to_export))

    def save_to_rom(self, output_path: Path) -> None:
        # Save and build all parsed entity files
        logging.info("Finalizing all entity files")
        self.finalize_entity_files()

        logging.info("Saving files to a new rom")
        self.finalize_string_tables()
        self.rom.saveToFile(output_path)
