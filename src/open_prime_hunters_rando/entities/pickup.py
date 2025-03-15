from open_prime_hunters_rando.entities.entity_data import ArtifactEntityData, ItemSpawnEntityData, LevelData

ITEM_TYPES_TO_IDS = {
    "HealthMedium": 0,
    "HealthSmall": 1,
    "HealthBig": 2,
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
    "UAExpansion": 18,
    "ArtifactKey": 19,
}


def _patch_header(entity_id: int, entity_type: int) -> bytearray:
    header = bytearray(3)

    header[0] = entity_type
    header[2] = entity_id

    return header


def _patch_item_spawn_data(entity_data: ItemSpawnEntityData, item_type: int) -> bytearray:
    data = bytearray(32)

    data[0] = 0xFF  # Always FF
    data[1] = 0xFF  # Always FF
    data[4] = item_type
    data[8] = entity_data.active
    data[9] = entity_data.has_base
    data[12] = 0x01  # max spawn count
    data[18] = entity_data.notify_entity_id
    data[20] = entity_data.collected_message

    return data


def _patch_artifact_data(entity_data: ArtifactEntityData, model_id: int, artifact_id: int) -> bytearray:
    data = bytearray(32)

    data[0] = model_id
    data[1] = artifact_id
    data[2] = entity_data.active
    data[3] = entity_data.has_base
    data[4] = entity_data.message1_target
    data[8] = entity_data.message1
    data[12] = entity_data.message2_target
    data[16] = entity_data.message2
    data[20] = entity_data.message3_target
    data[24] = entity_data.message3
    data[28] = 0xFF  # Always FF
    data[29] = 0xFF  # Always FF

    return data


def patch_pickups(entity_file: memoryview, level_data: LevelData, pickups: list) -> None:
    for pickup in pickups:
        entity_id = pickup["entity_id"]
        entity_type = pickup["entity_type"]

        for entity_data in level_data.entities:
            if entity_id == entity_data.entity_id:
                offset = entity_data.offset

                # Replace the existing header data with the modified header data
                header = _patch_header(entity_id, entity_type)
                entity_file[offset : offset + 3] = header

                # Update ItemSpawn entities
                if entity_type == 4:
                    data = _patch_item_spawn_data(
                        ItemSpawnEntityData,  # type: ignore
                        ITEM_TYPES_TO_IDS[pickup["item_type"]],
                    )
                # Update Artifact Entities
                elif entity_type == 17:
                    data = _patch_artifact_data(
                        ArtifactEntityData,  # type: ignore
                        pickup["model_id"],
                        pickup["artifact_id"],
                    )

                # The item data has an offset of 40 from the header
                data_offset = offset + 40
                # Replace the existing item data with the modified item data
                entity_file[data_offset : data_offset + 32] = data
