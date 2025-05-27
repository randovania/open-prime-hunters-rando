import logging
from pathlib import Path

from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.asm.asm_patching import NOP, create_asm_patch, read_asm_file
from open_prime_hunters_rando.version_checking import detect_rom

asm_patches = Path(__file__).parent.joinpath("files", "asm_patches")


def patch_arm9(rom: NintendoDSRom, configuration: dict) -> None:
    validated_rom = detect_rom(rom)
    logging.info("Patching arm9.bin")

    starting_items = configuration["starting_items"]
    game_patches = configuration["game_patches"]
    # Validate starting items
    _validate_starting_items(starting_items)

    etanks = starting_items["energy_tanks"]
    tanks_to_energy = etanks * 100 if etanks > 0 else 100
    starting_energy = tanks_to_energy.to_bytes(4, "little")

    starting_ammo = str(hex(starting_items["ammo"] * 10))[2:-1]

    reordered_instructions = read_asm_file("reordered_instructions.s")

    ARM9_PATCHES = {
        validated_rom["missiles_per_tank"]: (game_patches["missiles_per_tank"] * 10).to_bytes(),  # Missiles per tank
        validated_rom["starting_octoliths"]: _bitfield_to_hex(starting_items["octoliths"]),  # Starting Octoliths (0-8)
        validated_rom["starting_weapons"]: _bitfield_to_hex(starting_items["weapons"]),  # Starting weapons
        validated_rom["weapon_slots"]: NOP,  # Prevents deleting the weapons when changing Octoliths
        validated_rom["starting_ammo"]: bytes.fromhex(starting_ammo),  # Starting Universal Ammo
        validated_rom["starting_energy"]: NOP,  # Normally loads value of etank (100)
        validated_rom["starting_missiles"]: (starting_items["missiles"] * 10).to_bytes(),  # Starting Missiles
        validated_rom["reordered_instructions"]: create_asm_patch(
            reordered_instructions
        ),  # Changing R0 affects later instructions, so reorder
        validated_rom["unlock_planets"]: _unlock_planets(game_patches["unlock_planets"]),  # Unlock planets from start
        validated_rom["starting_energy_ptr"]: starting_energy,  # Starting energy - 1,
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
    bitfields = ["weapons", "octoliths"]
    # Validate weapons and octoliths bitfields
    for bitfield in bitfields:
        if len(starting_items[bitfield]) != 8:
            raise ValueError(
                f"Invalid starting {bitfield} bitfield. Must contain 8 numbers, got {len(starting_items[bitfield])}!"
            )

        for bitflag in starting_items[bitfield]:
            if bitflag not in ["0", "1"]:
                raise ValueError(f"Invalid starting {bitfield} bitfield. Must only contain 0 or 1, got {bitflag}!")

    # Validate starting ammo
    if starting_items["ammo"] > 400:
        raise ValueError(f"Starting ammo must be 400 or less! Got {starting_items['ammo']}")


def _bitfield_to_hex(bitfield: str) -> int:
    return int(bitfield, 2).to_bytes()


def _unlock_planets(unlock_planets: dict) -> int:
    planets = [
        unlock_planets["Arcterra"],  # Arcterra 1
        unlock_planets["Arcterra"],  # Arcterra 2
        unlock_planets["Vesper Defense Outpost"],  # Vesper Defense Outpost 1
        unlock_planets["Vesper Defense Outpost"],  # Vesper Defense Outpost 2
        True,  # Celestial Archives 1 (Always unlocked)
        True,  # Celestial Archives 2 (Always unlocked)
        unlock_planets["Alinos"],  # Alinos 1
        unlock_planets["Alinos"],  # Alinos 2
    ]

    fmt = "{:d}" * 8
    planets_to_unlock = fmt.format(*planets)
    return _bitfield_to_hex(planets_to_unlock)
