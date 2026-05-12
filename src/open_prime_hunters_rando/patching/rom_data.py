from enum import Enum

from ndspy.rom import NintendoDSRom


class InitEnemyHunterSpawns:
    def __init__(self, base_address: int) -> None:
        self.random_hunter_spawn_first_condition = base_address + 0x80
        self.random_hunter_spawn_game_state = base_address + 0x1E8


class PlayerPickupItems:
    def __init__(self, base_address: int) -> None:
        self.missile_launcher = base_address + 0x3E4
        self.nothing = base_address + 0x78C
        self.missiles_per_expansion = base_address + 0x8A0
        self.ammo_per_expansion = base_address + 0x8FC


class RoomTransitionEnd:
    def __init__(self, base_address: int) -> None:
        self.door_locking_condition = base_address + 0x70C


class InitSaveFile:
    def __init__(self, base_address: int) -> None:
        self.starting_octoliths = base_address + 0x3E
        self.starting_weapons = base_address + 0x46
        self.old_weapon_slots = base_address + 0x56
        self.starting_ammo = base_address + 0x6A
        self.old_starting_energy = base_address + 0x6E
        self.energy_cap = base_address + 0x7A
        self.starting_missiles = base_address + 0x86
        self.reordered_instructions = base_address + 0x92
        self.init_save_file_rewrite = base_address + 0xBA
        self.starting_energy_ptr = base_address + 0x276


class Arm9Addresses(InitEnemyHunterSpawns, PlayerPickupItems, RoomTransitionEnd, InitSaveFile):
    def __init__(self, revision_offset: int) -> None:
        # Base addresses for different functions
        init_enemy_hunter_spawn = 0x02015914
        player_pickup_items = 0x02019AB0
        room_transition_end = 0x02053430
        # This function starts at a different address based on the revision. US Rev0 is used as a base.
        init_save_file = 0x0205BC96 + revision_offset

        # Initialize each class using the base addresses
        InitEnemyHunterSpawns.__init__(self, init_enemy_hunter_spawn)
        PlayerPickupItems.__init__(self, player_pickup_items)
        RoomTransitionEnd.__init__(self, room_transition_end)
        InitSaveFile.__init__(self, init_save_file)


class OverlayOffsets:
    def __init__(self, revision_offset: int = 0x0) -> None:
        self.cloak = 0x01E20A + revision_offset
        self.affinity_weapon = 0x01E212 + revision_offset


class IdCode(Enum):
    AMHE = b"AMHE"
    AMHP = b"AMHP"
    AMHJ = b"AMHJ"
    AMHK = b"AMHK"


class Revision(Enum):
    REV0 = 0
    REV1 = 1


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

    def get_arm9_addresses(self) -> Arm9Addresses:
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
        return Arm9Addresses(revision_offset)

    def get_overlay_offsets(self) -> OverlayOffsets:
        revision_offset = 0x60 if self.version == Revision.REV1 else 0x00
        return OverlayOffsets(revision_offset)
