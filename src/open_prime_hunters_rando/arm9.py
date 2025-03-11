from ndspy.rom import NintendoDSRom


def patch_arm9(rom: NintendoDSRom, starting_items: str) -> None:
    ARM9_PATCHES = {
        0x0205C530: 0x00,   # Start game with 0/0 Missiles
        0x0205C4F0: int(starting_items, 2),  # Set starting items
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
