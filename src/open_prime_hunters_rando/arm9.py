from ndspy.rom import NintendoDSRom


def patch_arm9(rom: NintendoDSRom, starting_items: str) -> None:
    # Validate starting_items string
    _validate_starting_items(starting_items)

    ARM9_PATCHES = {
        0x0205C530: _patch_starting_missiles(starting_items),  # Modify starting Missile ammo (0 or 5)
        0x0205C4F0: int(starting_items, 2),  # Modify starting weapons
        0x0205C5DC: 0xFF,  # Unlock all planets from the start (excluding Oubliette)
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


def _validate_starting_items(starting_items: str) -> None:
    if len(starting_items) > 8:
        raise ValueError(f"Invalid starting items string. Must be a maximum length of 8, got {len(starting_items)}!")

    for bit_flag in starting_items:
        if bit_flag not in ["0", "1"]:
            raise ValueError(f"Invalid starting items string. String must only contain 0 or 1, got {bit_flag}!")


def _patch_starting_missiles(starting_items: str) -> int:
    missiles = starting_items[5]
    # Set the value of Missiles to 0 if not included
    return 0x00 if missiles == "0" else 0x32
