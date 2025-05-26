from enum import Enum

from ndspy.rom import NintendoDSRom


class Revision(Enum):
    AMHE = b"AMHE"
    AMHP = b"AMHP"
    AMHJ = b"AMHJ"
    AMHK = b"AMHK"


def validate_rom(rom: NintendoDSRom) -> dict:
    # Validate the rom
    id_code = rom.idCode
    # Use US addresses as a base, then add the offset difference based on region
    arm9_addresses: dict = {
        "missiles_per_tank": 0x0201A350,
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
    match id_code:
        case Revision.AMHE.value:
            return arm9_addresses
        case Revision.AMHP.value:
            _update_revision_offset(arm9_addresses, 0xAC)
        case Revision.AMHJ.value:
            _update_revision_offset(arm9_addresses, 0x14DC)
        case _:
            raise ValueError(f"Unsupported ROM detected. Detected {id_code!r}!")
    return arm9_addresses


def _update_revision_offset(arm9_addresses: dict, revision_offset: int) -> dict:
    for field, address in arm9_addresses.items():
        arm9_addresses[field] = address + revision_offset
    return arm9_addresses
