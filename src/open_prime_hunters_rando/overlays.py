import logging

import ndspy.code
from ndspy.rom import NintendoDSRom

OVERLAY_MODIFICATIONS = {
    # Overlay 2 handles Models and Scan Data
    2: [
        {
            # Assign the Missile Launcher scan entry to Affinity Weapon in the item_scan_id table
            "offset": 0x01E272,
            "value": 0x5.to_bytes(2, "little"),
        },
        {
            # Assign new Nothing scan entry to Nothing item (Cloak) in the item_scan_id table
            "offset": 0x01E26A,
            "value": 0x1DA.to_bytes(2, "little"),
        },
    ]
}


def patch_overlays(rom: NintendoDSRom) -> None:
    # Load the overlays
    overlays = rom.loadArm9Overlays()
    logging.info("Patching overlays")

    # Modify the overlays
    for overlay_id, offset_values in OVERLAY_MODIFICATIONS.items():
        overlay = overlays[overlay_id]
        for offset_value in offset_values:
            offset = offset_value["offset"]
            value = offset_value["value"]
            overlay.data[offset : offset + len(value)] = value

        # Save the modified file
        rom.files[overlay.fileID] = overlay.save(compress=True)

    # Save the overlays
    rom.arm9OverlayTable = ndspy.code.saveOverlayTable(overlays)
