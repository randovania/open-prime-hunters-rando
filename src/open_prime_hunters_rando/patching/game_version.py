import dataclasses
from collections.abc import Iterable
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


@dataclasses.dataclass(frozen=True)
class InitEnemyHunterSpawnsAddresses:
    random_hunter_spawn_first_condition: int
    random_hunter_spawn_game_state: int


@dataclasses.dataclass(frozen=True)
class PlayerPickupItemsAddresses:
    missile_launcher: int
    nothing: int
    missiles_per_expansion: int
    ammo_per_expansion: int


@dataclasses.dataclass(frozen=True)
class RoomTransitionEndAddresses:
    door_locking_condition: int


@dataclasses.dataclass(frozen=True)
class Mode1PCheckState:
    required_octoliths: int


@dataclasses.dataclass(frozen=True)
class InitSaveFileAddresses:
    starting_octoliths: int
    starting_weapons: int
    old_weapon_slots: int
    starting_ammo: int
    old_starting_energy: int
    energy_cap: int
    starting_missiles: int
    reordered_instructions: int
    init_save_file_rewrite: int
    starting_energy_ptr: int


@dataclasses.dataclass(frozen=True)
class OverlayOffsets:
    cloak: int
    affinity_weapon: int


@dataclasses.dataclass(frozen=True)
class MetroidHuntersTextFileOffsets:
    main_menu_textbox: int


@dataclasses.dataclass(frozen=True)
class GameVersion:
    id_code: IdCode
    revision: Revision
    description: str
    init_enemy_hunter_spawns_addresses: InitEnemyHunterSpawnsAddresses
    player_pickup_items_addresses: PlayerPickupItemsAddresses
    room_transition_end_addresses: RoomTransitionEndAddresses
    mode_1p_check_state: Mode1PCheckState
    init_save_file_addresses: InitSaveFileAddresses
    overlay_offsets: OverlayOffsets
    metroidhunters_text_file_offsets: MetroidHuntersTextFileOffsets


ALL_VERSIONS = [
    GameVersion(
        id_code=IdCode.AMHE,
        revision=Revision.REV0,
        description="USA 1.0",
        init_enemy_hunter_spawns_addresses=InitEnemyHunterSpawnsAddresses(
            random_hunter_spawn_first_condition=0x02015994,
            random_hunter_spawn_game_state=0x02015AFC,
        ),
        player_pickup_items_addresses=PlayerPickupItemsAddresses(
            missile_launcher=0x02019E94,
            nothing=0x0201A23C,
            missiles_per_expansion=0x0201A350,
            ammo_per_expansion=0x0201A3AC,
        ),
        room_transition_end_addresses=RoomTransitionEndAddresses(
            door_locking_condition=0x02053B3C,
        ),
        mode_1p_check_state=Mode1PCheckState(
            required_octoliths=0x02053FE0,
        ),
        init_save_file_addresses=InitSaveFileAddresses(
            starting_octoliths=0x0205BCD4,
            starting_weapons=0x0205BCDC,
            old_weapon_slots=0x0205BCEC,
            starting_ammo=0x0205BD00,
            old_starting_energy=0x0205BD04,
            energy_cap=0x0205BD10,
            starting_missiles=0x0205BD1C,
            reordered_instructions=0x0205BD28,
            init_save_file_rewrite=0x0205BD50,
            starting_energy_ptr=0x0205BF0C,
        ),
        overlay_offsets=OverlayOffsets(
            cloak=0x01E20A,
            affinity_weapon=0x01E212,
        ),
        metroidhunters_text_file_offsets=MetroidHuntersTextFileOffsets(
            main_menu_textbox=7944,
        ),
    ),
    GameVersion(
        id_code=IdCode.AMHE,
        revision=Revision.REV1,
        description="USA 1.1",
        init_enemy_hunter_spawns_addresses=InitEnemyHunterSpawnsAddresses(
            random_hunter_spawn_first_condition=0x02015994,
            random_hunter_spawn_game_state=0x02015AFC,
        ),
        player_pickup_items_addresses=PlayerPickupItemsAddresses(
            missile_launcher=0x02019E94,
            nothing=0x0201A23C,
            missiles_per_expansion=0x0201A350,
            ammo_per_expansion=0x0201A3AC,
        ),
        room_transition_end_addresses=RoomTransitionEndAddresses(
            door_locking_condition=0x02053B3C,
        ),
        mode_1p_check_state=Mode1PCheckState(
            required_octoliths=0x02054800,
        ),
        init_save_file_addresses=InitSaveFileAddresses(
            starting_octoliths=0x0205C4E8,
            starting_weapons=0x0205C4F0,
            old_weapon_slots=0x0205C500,
            starting_ammo=0x0205C514,
            old_starting_energy=0x0205C518,
            energy_cap=0x0205C524,
            starting_missiles=0x0205C530,
            reordered_instructions=0x0205C53C,
            init_save_file_rewrite=0x0205C564,
            starting_energy_ptr=0x0205C720,
        ),
        overlay_offsets=OverlayOffsets(
            cloak=0x01E26A,
            affinity_weapon=0x01E272,
        ),
        metroidhunters_text_file_offsets=MetroidHuntersTextFileOffsets(
            main_menu_textbox=6792,
        ),
    ),
    GameVersion(
        id_code=IdCode.AMHP,
        revision=Revision.REV0,
        description="Europe 1.0",
        init_enemy_hunter_spawns_addresses=InitEnemyHunterSpawnsAddresses(
            random_hunter_spawn_first_condition=0x02015994,
            random_hunter_spawn_game_state=0x02015AFC,
        ),
        player_pickup_items_addresses=PlayerPickupItemsAddresses(
            missile_launcher=0x02019E94,
            nothing=0x0201A23C,
            missiles_per_expansion=0x0201A350,
            ammo_per_expansion=0x0201A3AC,
        ),
        room_transition_end_addresses=RoomTransitionEndAddresses(
            door_locking_condition=0x02053B3C,
        ),
        mode_1p_check_state=Mode1PCheckState(
            required_octoliths=0x020547D4,
        ),
        init_save_file_addresses=InitSaveFileAddresses(
            starting_octoliths=0x0205C548,
            starting_weapons=0x0205C550,
            old_weapon_slots=0x0205C560,
            starting_ammo=0x0205C574,
            old_starting_energy=0x0205C578,
            energy_cap=0x0205C584,
            starting_missiles=0x0205C590,
            reordered_instructions=0x0205C59C,
            init_save_file_rewrite=0x0205C5C4,
            starting_energy_ptr=0x0205C780,
        ),
        overlay_offsets=OverlayOffsets(
            cloak=0x01E20A,
            affinity_weapon=0x01E212,
        ),
        metroidhunters_text_file_offsets=MetroidHuntersTextFileOffsets(
            main_menu_textbox=8012,
        ),
    ),
    GameVersion(
        id_code=IdCode.AMHP,
        revision=Revision.REV1,
        description="Europe 1.1",
        init_enemy_hunter_spawns_addresses=InitEnemyHunterSpawnsAddresses(
            random_hunter_spawn_first_condition=0x02015994,
            random_hunter_spawn_game_state=0x02015AFC,
        ),
        player_pickup_items_addresses=PlayerPickupItemsAddresses(
            missile_launcher=0x02019E94,
            nothing=0x0201A23C,
            missiles_per_expansion=0x0201A350,
            ammo_per_expansion=0x0201A3AC,
        ),
        room_transition_end_addresses=RoomTransitionEndAddresses(
            door_locking_condition=0x02053B3C,
        ),
        mode_1p_check_state=Mode1PCheckState(
            required_octoliths=0x02054800,
        ),
        init_save_file_addresses=InitSaveFileAddresses(
            starting_octoliths=0x0205C594,
            starting_weapons=0x0205C59C,
            old_weapon_slots=0x0205C5AC,
            starting_ammo=0x0205C5C0,
            old_starting_energy=0x0205C5C4,
            energy_cap=0x0205C5D0,
            starting_missiles=0x0205C5DC,
            reordered_instructions=0x0205C5E8,
            init_save_file_rewrite=0x0205C610,
            starting_energy_ptr=0x0205C7CC,
        ),
        overlay_offsets=OverlayOffsets(
            cloak=0x01E26A,
            affinity_weapon=0x01E272,
        ),
        metroidhunters_text_file_offsets=MetroidHuntersTextFileOffsets(
            main_menu_textbox=6792,
        ),
    ),
    GameVersion(
        id_code=IdCode.AMHJ,
        revision=Revision.REV0,
        description="Japanese 1.0",
        init_enemy_hunter_spawns_addresses=InitEnemyHunterSpawnsAddresses(
            random_hunter_spawn_first_condition=0x02015994,
            random_hunter_spawn_game_state=0x02015AFC,
        ),
        player_pickup_items_addresses=PlayerPickupItemsAddresses(
            missile_launcher=0x02019E94,
            nothing=0x0201A23C,
            missiles_per_expansion=0x0201A350,
            ammo_per_expansion=0x0201A3AC,
        ),
        room_transition_end_addresses=RoomTransitionEndAddresses(
            door_locking_condition=0x02053B3C,
        ),
        mode_1p_check_state=Mode1PCheckState(
            required_octoliths=0x02055A30,
        ),
        init_save_file_addresses=InitSaveFileAddresses(
            starting_octoliths=0x0205D9C4,
            starting_weapons=0x0205D9CC,
            old_weapon_slots=0x0205D9DC,
            starting_ammo=0x0205D9F0,
            old_starting_energy=0x0205D9F4,
            energy_cap=0x0205DA00,
            starting_missiles=0x0205DA0C,
            reordered_instructions=0x0205DA18,
            init_save_file_rewrite=0x0205DA40,
            starting_energy_ptr=0x0205DBFC,
        ),
        overlay_offsets=OverlayOffsets(
            cloak=0x01E20A,
            affinity_weapon=0x01E212,
        ),
        metroidhunters_text_file_offsets=MetroidHuntersTextFileOffsets(
            main_menu_textbox=7944,
        ),
    ),
]


def get_version(rom: NintendoDSRom, all_versions: Iterable[GameVersion]) -> GameVersion:
    id_code = IdCode(rom.idCode)
    revision = Revision(rom.version)

    if id_code not in {IdCode.AMHJ, IdCode.AMHK}:
        for version in all_versions:
            if id_code == version.id_code and revision == version.revision:
                return version

    raise ValueError(f"Unsupported ROM detected. Detected {id_code} Rev{revision}!")
