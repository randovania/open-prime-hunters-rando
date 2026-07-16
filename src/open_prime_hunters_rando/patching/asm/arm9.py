from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.patching.asm import read_bytes_from_file
from open_prime_hunters_rando.patching.asm.asm_patches import AsmPatches
from open_prime_hunters_rando.patching.game_version import GameVersion


def patch_arm9(rom: NintendoDSRom, version: GameVersion, configuration: dict) -> None:
    hunter = version.init_enemy_hunter_spawns_addresses
    pickup = version.player_pickup_items_addresses
    hud = version.hud_update_addresses
    room = version.room_transition_end_addresses
    save_file = version.init_save_file_addresses

    patches = AsmPatches(configuration, version)

    ARM9_PATCHES: dict[int, bytes] = {
        # Both Addresses below handle random hunter spawns
        hunter.random_hunter_spawn_first_condition: read_bytes_from_file("random_hunter_spawns.bin"),
        hunter.random_hunter_spawn_game_state: read_bytes_from_file("enemy_hunter_spawns.bin"),
        pickup.small_energy_refill_amount: patches.small_energy,  # Energy replenished by Small Energy
        pickup.medium_energy_refill_amount: patches.medium_energy,  # Energy replenished by Medium Energy
        pickup.large_energy_refill_amount: patches.large_energy,  # Energy replenished by Large Energy
        pickup.missile_launcher: patches.missile_launcher,  # Load instructions to create a custom Missile Launcher
        pickup.nothing: read_bytes_from_file("nothing.bin"),  # Add Nothing item
        pickup.missiles_per_expansion: patches.missiles_per_expansion,  # Missiles per expansion
        pickup.small_ammo_refill_amount: patches.small_ammo,  # Ammo replenished by Small Ammo
        pickup.large_ammo_refill_amount: patches.large_ammo,  # Ammo replenished by Large Ammo
        pickup.small_energy_play_sfx: patches.refill_play_sfx,  # Fixes pickup sfx if refill value is changed
        pickup.large_energy_play_sfx: patches.refill_play_sfx,  # Fixes pickup sfx if refill value is changed
        pickup.ammo_per_expansion: patches.ammo_per_expansion,  # UA per expansion
        # The next three addresses hijack Cloak hud code for the custom Missile Launcher
        hud.cloak_base_case: patches.cloak_base_case,
        hud.hud_up_cloak_base: patches.hud_up_cloak_base,
        hud.hud_up_weapon_unlocked_case_2: read_bytes_from_file("hud_up_weapon_unlocked_case_2.bin"),
        room.door_locking_condition: read_bytes_from_file(
            "door_locking_condition.bin"
        ),  # Handles the door locking code
        save_file.starting_octoliths: patches.starting_octoliths,  # Starting Octoliths (0-8)
        save_file.starting_weapons: patches.starting_weapons,  # Starting weapons
        # Overwrite weapon_slots to prevent deleting the weapons when
        # changing Octoliths. Sets the amount of starting Missiles
        save_file.old_weapon_slots: patches.starting_missiles,
        save_file.starting_ammo: patches.starting_ammo,  # Starting Universal Ammo
        save_file.old_starting_energy: read_bytes_from_file(
            "starting_missiles.bin"
        ),  # Normally loads value of etank (100). Now sets the starting missile ammo.
        save_file.energy_cap: read_bytes_from_file("energy_cap.bin"),  # Starting energy - 1 is now just starting energy
        save_file.starting_missiles: patches.starting_missiles,  # Sets the total capacity of starting Missiles
        save_file.reordered_instructions: read_bytes_from_file(
            "reordered_instructions.bin"
        ),  # Changing R0 affects later instructions, so reorder
        save_file.init_save_file_rewrite: patches.init_save_file_rewrite,  # Unlocked planets and starting artifacts
        save_file.starting_energy_ptr: patches.starting_energy,  # Starting energy - 1
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
