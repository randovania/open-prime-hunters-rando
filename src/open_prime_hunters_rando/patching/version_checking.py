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
        self.starting_octoliths = 0x0205BCD4 + revision_offset
        self.starting_weapons = 0x0205BCDC + revision_offset
        self.weapon_slots = 0x0205BCEC + revision_offset
        self.starting_ammo = 0x0205DB00 + revision_offset
        self.starting_energy = 0x0205BD04 + revision_offset
        self.starting_missiles = 0x0205BD1C + revision_offset
        self.reordered_instructions = 0x0205BD28 + revision_offset
        self.unlock_planets = 0x0205BDC8 + revision_offset
        self.starting_energy_ptr = 0x0205BF0C + revision_offset


def get_rom_save_data_addresses(rom: NintendoDSRom) -> SaveStoryAddresses:
    # Validate the rom
    id_code = rom.idCode
    match id_code:
        case Revision.AMHE.value:
            return SaveStoryAddresses(0x0)
        case Revision.AMHP.value:
            return SaveStoryAddresses(0x8C0)
        # TODO: Support Japanese version
        # case Revision.AMHJ.value:
        # return SaveStoryAddresses(0x1CF0)
        case _:
            raise ValueError(f"Unsupported ROM detected. Detected {id_code!r}!")
