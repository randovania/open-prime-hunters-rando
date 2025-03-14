from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.entity_data import get_data
from open_prime_hunters_rando.pickup import patch_pickups


def patch_entities(rom: NintendoDSRom, configuration: dict[str, dict]) -> None:
    for area_name, area_config in configuration.items():
        for level_name, level_config in area_config.items():
            for room_name, entity_groups in level_config.items():
                # Load the entity file for the room
                level_data = get_data(room_name)
                entity_file = memoryview(rom.getFileByName(f"levels/entities/{level_data.entity_file}_Ent.bin"))

                patch_pickups(entity_file, level_data, entity_groups["pickups"])

