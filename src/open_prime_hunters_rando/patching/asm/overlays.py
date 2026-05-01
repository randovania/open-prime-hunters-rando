import ndspy.code
from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.patching.rom_data import RomData


def patch_overlays(rom: NintendoDSRom) -> None:
    offsets = RomData(rom).get_overlay_offsets()

    OVERLAY_MODIFICATIONS: dict[int, list[dict[str, int]]] = {
        # Overlay 2 handles Models and Scan Data
        2: [
            {
                # Assign new Nothing scan entry to Nothing item (Cloak) in the item_scan_id table
                "offset": offsets.cloak,
                "value": 0x1DA,
            },
            {
                # Assign the Missile Launcher scan entry to Affinity Weapon in the item_scan_id table
                "offset": offsets.affinity_weapon,
                "value": 0x5,
            },
        ]
    }

    # Load the overlays
    overlays = rom.loadArm9Overlays()

    # Modify the overlays
    for overlay_id, offset_values in OVERLAY_MODIFICATIONS.items():
        overlay = overlays[overlay_id]
        for offset_value in offset_values:
            offset = offset_value["offset"]
            value = offset_value["value"].to_bytes(2, "little")
            overlay.data[offset : offset + len(value)] = value  # type: ignore[index]

        # Save the modified file
        rom.files[overlay.fileID] = overlay.save(compress=True)

    # Save the overlays
    rom.arm9OverlayTable = ndspy.code.saveOverlayTable(overlays)
