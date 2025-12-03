from open_prime_hunters_rando.entities.entity_type import DoorType, EntityFile, PaletteId


def patch_doors(entity_file: EntityFile, doors: list, room_name: str) -> None:
    for door in doors:
        entity_id = door["entity_id"]
        palette_id = PaletteId(door["palette_id"])

        entity = entity_file.get_entity(entity_id).door_data()

        # Break if trying to change weakness of Morph Ball or Boss doors
        if entity.door_type not in (DoorType.STANDARD, DoorType.THIN):
            raise ValueError(
                f"Unable to patch entity {entity_id} in {room_name}. Only Standard and Thin door types can be modified."
            )
        # If the new type is the same as the original type, skip changing it
        if palette_id == entity.palette_id:
            continue

        # Change the weakness
        entity.palette_id = palette_id

        # Unlock doors that are changed to Power Beam
        if palette_id == PaletteId.POWER_BEAM:
            entity.locked = False
        # Activate and lock doors changed to another weapon
        else:
            entity.locked = True
