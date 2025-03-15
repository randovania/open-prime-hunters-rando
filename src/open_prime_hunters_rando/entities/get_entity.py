def get_entity(entity_file: memoryview, new_entity_id: int) -> tuple[int, int]:
    num_entities = entity_file[0x04]
    entry_length = 0x18

    i = 1
    entry_start = 0x24
    entry_end = 0x3C
    while i <= num_entities:
        entity_entry = entity_file[entry_start:entry_end]
        data_offset = int.from_bytes(entity_entry[0x14:0x16], "little")
        found_entity_type = entity_file[data_offset]
        found_entity_id = entity_file[data_offset + 2]
        if found_entity_id != new_entity_id:
            entry_start += entry_length
            entry_end += entry_length
            i += 1
        else:
            break

    return data_offset, found_entity_type
