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
    arm9_addresses: dict = {}
    match id_code:
        case Revision.AMHE.value:
            arm9_addresses["starting_weapons"] = 0x0205C4F0
            arm9_addresses["starting_missiles"] = 0x0205C530
            arm9_addresses["unlock_planets"] = 0x0205C5DC
        case Revision.AMHP.value:
            arm9_addresses["starting_weapons"] = 0x0205C59C
            arm9_addresses["starting_missiles"] = 0x0205C5DC
            arm9_addresses["unlock_planets"] = 0x0205C688
        case Revision.AMHJ.value:
            arm9_addresses["starting_weapons"] = 0x0205D9CC
            arm9_addresses["starting_missiles"] = 0x0205DA0C
            arm9_addresses["unlock_planets"] = 0x0205DAB8
        case _:
            raise ValueError(f"Unsupported ROM detected. Detected {id_code!r}!")
    return arm9_addresses
