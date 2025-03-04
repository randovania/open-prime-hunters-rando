from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.entity_data import get_data

ITEM_TYPES_TO_IDS = {
    "None": -1,
    "HealthMedium": 0,
    "HealthSmall": 1,
    "HealthBig": 2,
    "DoubleDamage": 3,
    "EnergyTank": 4,
    "VoltDriver": 5,
    "MissileExpansion": 6,
    "Battlehammer": 7,
    "Imperialist": 8,
    "Judicator": 9,
    "Magmaul": 10,
    "ShockCoil": 11,
    "OmegaCannon": 12,
    "UASmall": 13,
    "UABig": 14,
    "MissileSmall": 15,
    "MissileBig": 16,
    "Cloak": 17,
    "UAExpansion": 18,
    "ArtifactKey": 19,
    "Deathalt": 20,
    "AffinityWeapon": 21,
    "PickWpnMissile": 22,
}


ENTITY_TYPES_TO_IDS = {"item_spawns": 4, "artifacts": 17}


class ItemSpawnEntity:
    @classmethod
    def entity_header(cls, entity_type: int, entity_id: int) -> bytearray:
        header = bytearray(3)
        mv = memoryview(header)

        mv[0] = entity_type
        # mv[1] is always 0
        mv[2] = entity_id

        return header

    @classmethod
    def entity_data(cls, item_type: int, collected_message: int, enabled: bool, has_base: bool) -> bytearray:
        data = bytearray(32)
        mv = memoryview(data)

        mv[0] = 255  # Always FF
        mv[1] = 255  # Always FF
        mv[4] = item_type
        mv[8] = enabled
        mv[9] = has_base
        mv[12] = 1  # max spawn count
        mv[20] = collected_message

        return data


def patch_pickups(rom: NintendoDSRom, configuration: dict[str, dict]) -> None:
    for area_name, area_config in configuration.items():
        for level_name, level_config in area_config.items():
            for room_name, entities in level_config.items():
                # Load the entity file
                level_data = get_data(room_name)
                entity_file = rom.getFileByName(f"levels/entities/{level_data.entity_file}_Ent.bin")
                mv = memoryview(entity_file)
                for entity_type in entities:
                    # Modify ItemSpawns
                    if entity_type == "item_spawns":
                        type = ENTITY_TYPES_TO_IDS[entity_type]
                        for entity in entities["item_spawns"]:
                            entity_id = entity["entity_id"]
                            item_type = ITEM_TYPES_TO_IDS[entity["item_type"]]
                            collected_message = 0
                            for entity_data in level_data.entities:
                                if entity_id == entity_data.entity_id:
                                    header = ItemSpawnEntity.entity_header(type, entity_id)
                                    data = ItemSpawnEntity.entity_data(
                                        item_type, collected_message, entity_data.enabled, entity_data.has_base
                                    )
                                    offset = entity_data.offset
                                    # The item data has an offset of 40 from the header
                                    data_offset = offset + 40
                                    mv[offset : offset + 3] = header
                                    mv[data_offset : data_offset + 32] = data
