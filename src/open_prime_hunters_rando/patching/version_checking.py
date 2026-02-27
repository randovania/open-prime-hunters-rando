from enum import Enum

from ndspy.rom import NintendoDSRom


class Revision(Enum):
    AMHE = b"AMHE"
    AMHP = b"AMHP"
    AMHJ = b"AMHJ"
    AMHK = b"AMHK"


class SaveStoryAddresses:
    def __init__(self, revision_offset: int) -> None:
        # Addresses that are consistent across all revisions
        self.missile_launcher = 0x02019E94
        self.nothing = 0x0201A23C
        self.missiles_per_expansion = 0x0201A350
        self.ammo_per_expansion = 0x0201A3AC

        # Addresses that are different across revisions (Using US as a base)
        self.starting_octoliths = 0x0205C4E8 + revision_offset
        self.starting_weapons = 0x0205C4F0 + revision_offset
        self.weapon_slots = 0x0205C500 + revision_offset
        self.starting_ammo = 0x0205C514 + revision_offset
        self.starting_energy = 0x0205C518 + revision_offset
        self.starting_missiles = 0x0205C530 + revision_offset
        self.reordered_instructions = 0x0205C53C + revision_offset
        self.unlock_planets = 0x0205C5DC + revision_offset
        self.starting_energy_ptr = 0x0205C720 + revision_offset


def get_rom_save_data_addresses(rom: NintendoDSRom) -> SaveStoryAddresses:
    # Validate the rom
    id_code = rom.idCode
    match id_code:
        case Revision.AMHE.value:
            return SaveStoryAddresses(0x0)
        case Revision.AMHP.value:
            return SaveStoryAddresses(0xAC)
        case Revision.AMHJ.value:
            return SaveStoryAddresses(0x14DC)
        case _:
            raise ValueError(f"Unsupported ROM detected. Detected {id_code!r}!")
