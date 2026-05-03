from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.patching.asm import read_bytes_from_file
from open_prime_hunters_rando.patching.asm.asm_patches import AsmPatches
from open_prime_hunters_rando.patching.rom_data import RomData


def patch_arm9(rom: NintendoDSRom, configuration: dict) -> None:
    addresses = RomData(rom).get_story_save_addresses()
    patches = AsmPatches(configuration)

    ARM9_PATCHES: dict[int, bytes] = {
        addresses.missiles_per_expansion: patches.missiles_per_expansion,  # Missiles per expansion
        addresses.ammo_per_expansion: patches.ammo_per_expansion,  # UA per expansion
        addresses.starting_octoliths: patches.starting_octoliths,  # Starting Octoliths (0-8)
        addresses.starting_weapons: patches.starting_weapons,  # Starting weapons
        # Overwrite weapon_slots to prevent deleting the weapons when
        # changing Octoliths. Sets the amount of starting Missiles
        addresses.old_weapon_slots: patches.starting_missiles,
        addresses.starting_ammo: patches.starting_ammo,  # Starting Universal Ammo
        addresses.old_starting_energy: read_bytes_from_file(
            "starting_missiles.bin"
        ),  # Normally loads value of etank (100). Now sets the starting missile ammo.
        addresses.energy_cap: read_bytes_from_file("energy_cap.bin"),  # Starting energy - 1 is now just starting energy
        addresses.starting_missiles: patches.starting_missiles,  # Sets the total capacity of starting Missiles
        addresses.reordered_instructions: read_bytes_from_file(
            "reordered_instructions.bin"
        ),  # Changing R0 affects later instructions, so reorder
        addresses.unlock_planets: patches.unlock_planets,  # Unlock planets from start
        addresses.starting_energy_ptr: patches.starting_energy,  # Starting energy - 1
        addresses.missile_launcher: patches.missile_launcher,  # Load instructions to create a custom Missile Launcher
        addresses.nothing: read_bytes_from_file("nothing.bin"),  # Add Nothing item
        # Addresses below handle random hunter spawns and locking doors
        addresses.random_hunter_spawn_first_condition: read_bytes_from_file("random_hunter_spawns.bin"),
        addresses.random_hunter_spawn_game_state: read_bytes_from_file("enemy_hunter_spawns.bin"),
        addresses.door_locking_condition: read_bytes_from_file("door_locking_condition.bin"),
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
