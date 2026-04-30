from enum import Enum

from ndspy.rom import NintendoDSRom


class IdCode(Enum):
    AMHE = b"AMHE"
    AMHP = b"AMHP"
    AMHJ = b"AMHJ"
    AMHK = b"AMHK"


class Revision(Enum):
    REV0 = 0
    REV1 = 1


class StorySaveAddresses:
    def __init__(self, revision_offset: int) -> None:
        # Addresses that are consistent across all revisions
        self.init_enemy_hunter_spawns = 0x02015914
        self.random_hunter_spawn_first_condition = 0x02015994
        self.random_hunter_spawn_game_state = 0x02015AFC
        self.missile_launcher = 0x02019E94
        self.nothing = 0x0201A23C
        self.missiles_per_expansion = 0x0201A350
        self.ammo_per_expansion = 0x0201A3AC
        self.door_locking_condition = 0x02053B3C

        # Addresses that are different across revisions (Using US 1.0 as a base)
        self.story_save_data_start = 0x0205BC96 + revision_offset
        self.starting_octoliths = 0x0205BCD4 + revision_offset
        self.starting_weapons = 0x0205BCDC + revision_offset
        self.weapon_slots = 0x0205BCEC + revision_offset
        self.starting_ammo = 0x0205BD00 + revision_offset
        self.starting_energy = 0x0205BD04 + revision_offset
        self.starting_missiles = 0x0205BD1C + revision_offset
        self.reordered_instructions = 0x0205BD28 + revision_offset
        self.unlock_planets = 0x0205BDC8 + revision_offset
        self.starting_energy_ptr = 0x0205BF0C + revision_offset


class OverlayOffsets:
    def __init__(self, revision_offset: int = 0x0) -> None:
        self.cloak = 0x01E20A + revision_offset
        self.affinity_weapon = 0x01E212 + revision_offset


class RomData:
    def __init__(self, rom: NintendoDSRom) -> None:
        self.rom = rom
        self._id_code = rom.idCode
        self._version = rom.version

    @property
    def id_code(self) -> IdCode:
        return IdCode(self._id_code)

    @property
    def version(self) -> Revision:
        return Revision(self._version)

    def get_story_save_addresses(self) -> StorySaveAddresses:
        match (self.id_code, self.version):
            case (IdCode.AMHE, Revision.REV0):
                revision_offset = 0x0
            case (IdCode.AMHE, Revision.REV1):
                revision_offset = 0x814
            case (IdCode.AMHP, Revision.REV0):
                revision_offset = 0x874
            case (IdCode.AMHP, Revision.REV1):
                revision_offset = 0x8C0
            # case (IdCode.AMHJ, Revision.REV0):
            #     revision_offset = 0x1CF0
            case _:
                raise ValueError(f"Unsupported ROM detected. Detected {self.id_code} Rev{self.version.value}!")
        return StorySaveAddresses(revision_offset)

    def get_overlay_offsets(self) -> OverlayOffsets:
        revision_offset: int = 0x0
        if self.version == Revision.REV1:
            revision_offset = 0x60
        return OverlayOffsets(revision_offset)
