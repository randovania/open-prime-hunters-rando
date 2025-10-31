from enum import Enum

from ndspy.rom import NintendoDSRom


class Revision(Enum):
    AMHE = b"AMHE"
    AMHP = b"AMHP"
    AMHJ = b"AMHJ"
    AMHK = b"AMHK"


def detect_rom(rom: NintendoDSRom) -> dict:
    # Validate the rom
    id_code = rom.idCode
    match id_code:
        case Revision.AMHE.value:
            return _update_revision_offsets()
        case Revision.AMHP.value:
            return _update_revision_offsets(0xAC)
        case Revision.AMHJ.value:
            return _update_revision_offsets(0x14DC)
        case _:
            raise ValueError(f"Unsupported ROM detected. Detected {id_code!r}!")


def _update_revision_offsets(revision_offset: int = 0) -> dict:
    # These addresses pertain to the StorySaveData
    # Use US addresses as a base, then add the offset difference based on region

    # Addresses that are consistent across all revisions
    story_save_data_addresses: dict = {
        "missiles_per_tank": 0x0201A350,
        "ammo_per_tank": 0x0201A3AC,
    }

    # Addresses that are different across all revisisions
    revision_addresses: dict = {
        "starting_octoliths": 0x0205C4E8,
        "starting_weapons": 0x0205C4F0,
        "weapon_slots": 0x0205C500,
        "starting_ammo": 0x0205C514,
        "starting_energy": 0x0205C518,
        "starting_missiles": 0x0205C530,
        "reordered_instructions": 0x0205C53C,
        "unlock_planets": 0x0205C5DC,
        "starting_energy_ptr": 0x0205C720,
    }
    for field, address in revision_addresses.items():
        story_save_data_addresses[field] = address + revision_offset
    return story_save_data_addresses
