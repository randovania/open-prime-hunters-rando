import ndspy.code
from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.patching.asm import NOP
from open_prime_hunters_rando.patching.game_version import GameVersion


def patch_overlays(rom: NintendoDSRom, version: GameVersion) -> None:
    OVERLAY_MODIFICATIONS: dict[int, dict[int, int | bytes]] = {
        # Gameplay
        2: {
            # Assign new Nothing scan entry to Cloak in the item_scan_id table
            version.overlay2_offsets.cloak: 0x1DA,
            # Assign the Missile Launcher scan entry to Affinity Weapon in the item_scan_id table
            version.overlay2_offsets.affinity_weapon: 0x5,
        },
        # Single Player Entities
        8: {
            # Prevent the Octolith pickup movie from playing
            version.overlay8_offsets.octolith_start_movie: NOP * 11,
            # Remove the layer state changes from collecting an Ocolith
            version.overlay8_offsets.octolith_set_game_state: NOP * 11,
        },
    }

    # Load the overlays
    overlays = rom.loadArm9Overlays()

    # Modify the overlays
    for overlay_id, offset_values in OVERLAY_MODIFICATIONS.items():
        overlay = overlays[overlay_id]
        for offset, value in offset_values.items():
            if isinstance(value, int):
                value_as_bytes = value.to_bytes(2, "little")
            else:
                value_as_bytes = value
            overlay.data[offset : offset + len(value_as_bytes)] = value_as_bytes  # type: ignore[index]

        # Save the modified file
        rom.files[overlay.fileID] = overlay.save(compress=True)

    # Save the overlays
    rom.arm9OverlayTable = ndspy.code.saveOverlayTable(overlays)
