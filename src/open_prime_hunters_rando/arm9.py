from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.version_checking import validate_rom


def patch_arm9(rom: NintendoDSRom, starting_items: dict) -> None:
    arm9_addresses = validate_rom(rom)
    # Validate starting_items string
    _validate_starting_items(starting_items)

    ARM9_PATCHES = {
        arm9_addresses["starting_weapons"]: int(starting_items["weapons_string"], 2),  # Modify starting weapons
        arm9_addresses["starting_missiles"]: _patch_starting_missiles(starting_items),  # Modify starting Missile ammo
        arm9_addresses["unlock_planets"]: 0xFF,  # Unlock all planets from the start (excluding Oubliette)
    }

    # Decompress arm9.bin for editing
    arm9 = rom.loadArm9()
    # Load the addresses and bytes
    for target_address, bytes_to_change in ARM9_PATCHES.items():
        # Search for the offset to modify
        for section in arm9.sections:
            if section.ramAddress <= target_address < section.ramAddress + len(section.data):
                offset_in_section = target_address - section.ramAddress
                section.data = bytearray(section.data)
                # Edit the offset with the new bytes
                section.data[offset_in_section] = bytes_to_change
                break

    # Save arm9.bin with the new changes
    rom.arm9 = arm9.save()


def _validate_starting_items(starting_items: dict) -> None:
    if len(starting_items["weapons_string"]) != 8:
        raise ValueError(f"Invalid starting items string. Must contain 8 numbers, got {len(starting_items)}!")

    for bit_flag in starting_items["weapons_string"]:
        if bit_flag not in ["0", "1"]:
            raise ValueError(f"Invalid starting items string. String must only contain 0 or 1, got {bit_flag}!")


def _patch_starting_missiles(starting_items: dict) -> int:
    missiles = starting_items["weapons_string"][5]
    missile_ammo = starting_items["starting_ammo"]["Missiles"]
    # Set the value of Missiles to 0 if the missile bit flag is 0
    return 0 if missiles == "0" else missile_ammo
