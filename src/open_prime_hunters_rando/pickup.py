from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.entity_data import EntityData, get_data

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
    mv[2] = entity_id

    return header


class ItemSpawnEntity:
    @classmethod
    def patch_data(cls, entity_data: EntityData, item_type: int) -> bytearray:
        data = bytearray(32)
        mv = memoryview(data)

        mv[0] = 255  # Always FF
        mv[1] = 255  # Always FF
        mv[4] = item_type
        mv[8] = entity_data.active
        mv[9] = entity_data.has_base
        mv[12] = 1  # max spawn count

        # Messages
        if entity_data.item_spawn_messages is not None:
            mv[18] = entity_data.item_spawn_messages.notify_entity_id
            mv[20] = entity_data.item_spawn_messages.collected_message

        return data


class ArtifactEntity:
    @classmethod
    def patch_data(cls, entity_data: EntityData, model_id: int, artifact_id: int) -> bytearray:
        data = bytearray(32)
        mv = memoryview(data)

        mv[0] = model_id
        mv[1] = artifact_id
        mv[2] = entity_data.active
        mv[3] = entity_data.has_base
        mv[28] = 255  # Always FF
        mv[29] = 255  # Always FF

        # Messages
        if entity_data.artifact_messages is not None:
            mv[4] = entity_data.artifact_messages.message1_target
            mv[8] = entity_data.artifact_messages.message1
            mv[12] = entity_data.artifact_messages.message2_target
            mv[16] = entity_data.artifact_messages.message2
            mv[20] = entity_data.artifact_messages.message3_target
            mv[24] = entity_data.artifact_messages.message3

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
                                if entity_type == "ItemSpawn":
                                    item_type = ITEM_TYPES_TO_IDS[entity["item_type"]]
                                    data = ItemSpawnEntity.patch_data(entity_data, item_type)
                                elif entity_type == "Artifact":
                                    model_id = entity["model_id"]
                                    artifact_id = entity["artifact_id"]
                                    data = ArtifactEntity.patch_data(entity_data, model_id, artifact_id)
                                else:
                                    raise KeyError(f"Unknown entity type '{entity['entity_type']}'.")
                                offset = entity_data.offset
                                # Replace the existing header data with the modified header data
                                mv[offset : offset + 3] = header
                                # The item data has an offset of 40 from the header
                                data_offset = offset + 40
                                # Replace the existing item data with the modified item data
                                mv[data_offset : data_offset + 32] = data
