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

ENTITY_TYPES_TO_IDS = {
    "ItemSpawn": 4,
    "Artifact": 17,
}


def patch_header(entity_id: int, entity_type: int) -> bytearray:
    header = bytearray(3)
    mv = memoryview(header)

    mv[0] = entity_type
    # mv[1] is always 0
    mv[2] = entity_id

    return header


def patch_item_spawn_entity(item_type: int, collected_message: int, active: bool, has_base: bool) -> bytearray:
    data = bytearray(32)
    mv = memoryview(data)

    mv[0] = 255  # Always FF
    mv[1] = 255  # Always FF
    mv[4] = item_type
    mv[8] = active
    mv[9] = has_base
    mv[12] = 1  # max spawn count
    mv[20] = collected_message

    return data


def patch_artifact_entity(
    model_id: int, artifact_id: int, active: bool, has_base: bool, collected_message: int
) -> bytearray:
    data = bytearray(32)
    mv = memoryview(data)

    mv[0] = model_id
    mv[1] = artifact_id
    mv[2] = active
    mv[3] = has_base
    mv[8] = collected_message
    mv[28] = 255  # Always FF
    mv[29] = 255  # Always FF

    return data


def patch_pickups(rom: NintendoDSRom, configuration: dict[str, dict]) -> None:
    for area_name, area_config in configuration.items():
        for level_name, level_config in area_config.items():
            for room_name, pickup_config in level_config.items():
                # Load the entity file for the room
                level_data = get_data(room_name)
                entity_file = rom.getFileByName(f"levels/entities/{level_data.entity_file}_Ent.bin")
                mv = memoryview(entity_file)
                for entity_group, entities in pickup_config.items():
                    for entity in entities:
                        entity_id = entity["entity_id"]
                        entity_type = entity["entity_type"]
                        converted_entity_type = ENTITY_TYPES_TO_IDS[entity_type]
                        for entity_data in level_data.entities:
                            if entity_id == entity_data.entity_id:
                                header = patch_header(entity_id, converted_entity_type)
                                collected_message = 0
                                if entity_type == "ItemSpawn":
                                    item_type = ITEM_TYPES_TO_IDS[entity["item_type"]]
                                    data = patch_item_spawn_entity(
                                        item_type, collected_message, entity_data.active, entity_data.has_base
                                    )
                                elif entity_type == "Artifact":
                                    model_id = entity["model_id"]
                                    artifact_id = entity["artifact_id"]
                                    data = patch_artifact_entity(
                                        model_id,
                                        artifact_id,
                                        entity_data.active,
                                        entity_data.has_base,
                                        collected_message,
                                    )
                                else:
                                    raise KeyError(f"Unknown entity type '{entity['entity_type']}'.")
                                offset = entity_data.offset
                                # The item data has an offset of 40 from the header
                                data_offset = offset + 40
                                mv[offset : offset + 3] = header
                                mv[offset : offset + 3]
                                mv[data_offset : data_offset + 32] = data
