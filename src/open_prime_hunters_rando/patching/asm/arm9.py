from pathlib import Path

from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.patching.asm import generate_arm_add_bytes
from open_prime_hunters_rando.patching.version_checking import get_rom_save_data_addresses

asm_patches = Path(__file__).parent.parent.parent.joinpath("files", "asm_patches")

NOP = bytes.fromhex("00F020E3")


def _read_bytes_from_file(asm_patch: bytes) -> bytes:
    return Path(asm_patches / asm_patch).read_bytes()


def patch_arm9(rom: NintendoDSRom, configuration: dict) -> None:
    addresses = get_rom_save_data_addresses(rom)

    starting_items = configuration["starting_items"]
    game_patches = configuration["game_patches"]
    ammo_sizes = configuration["ammo_sizes"]

    # Validate starting items
    _validate_starting_items(starting_items)

    etanks = starting_items["energy_tanks"]
    tanks_to_energy = etanks * 100 if etanks > 0 else 100
    starting_energy = tanks_to_energy.to_bytes(4, "little")

    starting_ammo = str(hex(starting_items["ammo"] * 10))[2:-1]

    # Missile Launcher (Direct, searching for original #50 / 0x32 20)
    missile_launcher_instructions = generate_arm_add_bytes(ammo_sizes["missile_launcher"])
    custom_missile_launcher = _read_bytes_from_file("missile_launcher.bin")
    custom_missile_launcher = custom_missile_launcher.replace(b"\x32\x20\x82\xe2", missile_launcher_instructions)

    # Missile Expansion (x10, searching for placeholder #0xFF / 0xFF 20)
    missile_expansion_instructions = generate_arm_add_bytes(ammo_sizes["missile_expansion"], multiply=True)
    missiles_per_expansion = _read_bytes_from_file("ammo_per_expansion.bin")
    missiles_per_expansion = missiles_per_expansion.replace(b"\xff\x20\x82\xe2", missile_expansion_instructions)

    # UA Expansion (x10, searching for placeholder #0xFF / 0xFF 20)
    ua_expansion_instructions = generate_arm_add_bytes(ammo_sizes["ua_expansion"], multiply=True)
    ammo_per_expansion = _read_bytes_from_file("ammo_per_expansion.bin")
    ammo_per_expansion = ammo_per_expansion.replace(b"\xff\x20\x82\xe2", ua_expansion_instructions)

    ARM9_PATCHES: dict[int, bytes] = {
        addresses.missiles_per_expansion: missiles_per_expansion,  # Missiles per expansion
        addresses.ammo_per_expansion: ammo_per_expansion,  # UA per expansion
        addresses.starting_octoliths: _bitfield_to_hex(starting_items["octoliths"]),  # Starting Octoliths (0-8)
        addresses.starting_weapons: _bitfield_to_hex(starting_items["weapons"]),  # Starting weapons
        addresses.weapon_slots: NOP,  # Prevents deleting the weapons when changing Octoliths
        addresses.starting_ammo: bytes.fromhex(starting_ammo),  # Starting Universal Ammo
        addresses.starting_energy: NOP,  # Normally loads value of etank (100)
        addresses.starting_missiles: (starting_items["missiles"] * 10).to_bytes(),  # Starting Missiles
        addresses.reordered_instructions: _read_bytes_from_file(
            "reordered_instructions.bin"
        ),  # Changing R0 affects later instructions, so reorder
        addresses.unlock_planets: _unlock_planets(game_patches["unlock_planets"]),  # Unlock planets from start
        addresses.starting_energy_ptr: starting_energy,  # Starting energy - 1
        addresses.missile_launcher: custom_missile_launcher,  # Load instructions to create a custom Missile Launcher
        addresses.nothing: _read_bytes_from_file("nothing.bin"),  # Add Nothing item
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


def _bitfield_to_hex(bitfield: str) -> bytes:
    return int(bitfield, 2).to_bytes()


def _unlock_planets(unlock_planets: dict) -> bytes:
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
