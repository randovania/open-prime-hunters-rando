from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.version_checking import validate_rom


def patch_arm9(rom: NintendoDSRom, starting_items: dict) -> None:
    init = validate_rom(rom)
    # Validate starting_items string
    _validate_starting_items(starting_items)

    starting_energy = starting_items["energy"].to_bytes(4, "little")
    starting_ammo = str(hex(starting_items["ammo"] * 10))[2:-1]
    starting_missiles = starting_items["missiles"].to_bytes()

    ARM9_PATCHES = {
        init["starting_ammo"]: bytes.fromhex(starting_ammo),  # Starting UA Ammo
        init["starting_energy"]: bytes.fromhex("00F020E3"),  # NOP (Normally loads value of etank (100))
        init["starting_weapons"]: int(starting_items["weapons"], 2).to_bytes(),  # Starting weapons
        init["starting_missiles"]: starting_missiles,  # Starting Missile ammo
        init["unlock_planets"]: bytes.fromhex("FF"),  # Unlock all planets from the start (excluding Oubliette)
        init["starting_energy_ptr"]: starting_energy,  # Starting energy - 1
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
                section.data[offset_in_section : offset_in_section + len(bytes_to_change)] = bytes_to_change
                break

    # Save arm9.bin with the new changes
    rom.arm9 = arm9.save()


def _validate_starting_items(starting_items: dict) -> None:
    # Validate weapons string
    if len(starting_items["weapons"]) != 8:
        raise ValueError(f"Invalid starting items string. Must contain 8 numbers, got {len(starting_items)}!")

    for bit_flag in starting_items["weapons"]:
        if bit_flag not in ["0", "1"]:
            raise ValueError(f"Invalid starting items string. String must only contain 0 or 1, got {bit_flag}!")

    # Validate starting ammo
    if starting_items["ammo"] > 400:
        raise ValueError(f"Starting ammo must be 400 or less! Got {starting_items['ammo']}")
