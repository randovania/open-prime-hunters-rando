from open_prime_hunters_rando.entities.entity_type import EntityFile, PaletteId


def patch_doors(entity_file: EntityFile, doors: list) -> None:
    for door in doors:
        entity_id = door["entity_id"]
        palette_id = door["palette_id"]

        entity = entity_file.get_entity(entity_id)
        data = entity.data

        # If the new type is the same as the original type, skip changing it
        if palette_id == data.palette_id:
            continue

        # Change the weakness
        data.palette_id = PaletteId(palette_id)

        # Unlock doors that are changed to Power Beam
        if palette_id == PaletteId.POWER_BEAM:
            data.locked = False
        # Activate and lock doors changed to another weapon
        else:
            data.locked = True
