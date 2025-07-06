import logging
from pathlib import Path

import keystone
from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.version_checking import validate_rom

NOP = bytes.fromhex("00F020E3")

asm_patches = Path(__file__).parent.joinpath("files", "asm_patches")


def create_asm_patch(code: str) -> bytes:
    assembler = keystone.Ks(keystone.KS_ARCH_ARM, keystone.KS_MODE_ARM + keystone.KS_MODE_LITTLE_ENDIAN)
    encoding, count = assembler.asm(code)
    return bytes(encoding)


def _read_asm_file(file: str) -> str:
    return asm_patches.joinpath(file).read_text()


def patch_arm9(rom: NintendoDSRom, configuration: dict) -> None:
    arm9 = validate_rom(rom)
    logging.info("Patching arm9.bin")

    starting_items = configuration["starting_items"]
    game_patches = configuration["game_patches"]
    # Validate starting items
    _validate_starting_items(starting_items)

    etanks = starting_items["energy_tanks"]
    tanks_to_energy = etanks * 100 if etanks > 0 else 100
    starting_energy = tanks_to_energy.to_bytes(4, "little")

    starting_ammo = str(hex(starting_items["ammo"] * 10))[2:-1]

    reordered_instructions = _read_asm_file("reordered_instructions.s")

    ARM9_PATCHES = {
        arm9["starting_octoliths"]: _bitfield_to_hex(starting_items["octoliths"]),  # Starting Octoliths by changing R0
        arm9["starting_weapons"]: _bitfield_to_hex(starting_items["weapons"]),  # Starting weapons
        arm9["weapon_slots"]: NOP,  # Prevents deleting the weapons when changing Octoliths
        arm9["starting_ammo"]: bytes.fromhex(starting_ammo),  # Starting UA
        arm9["starting_energy"]: NOP,  # Normally loads value of etank (100)
        arm9["starting_missiles"]: (starting_items["missiles"] * 10).to_bytes(),  # Starting Missiles
        arm9["reordered_instructions"]: create_asm_patch(
            reordered_instructions
        ),  # Changing R0 affects later instructions, so reorder
        arm9["unlock_planets"]: _unlock_planets(game_patches["unlock_planets"]),  # Unlock planets from the start
        arm9["starting_energy_ptr"]: starting_energy,  # Starting energy - 1,
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
