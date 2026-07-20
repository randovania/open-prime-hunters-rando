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
    small_energy_refill_amount: int
    medium_energy_refill_amount: int
    large_energy_refill_amount: int
    missile_launcher: int
    nothing: int
    missiles_per_expansion: int
    small_ammo_refill_amount: int
    large_ammo_refill_amount: int
    small_energy_play_sfx: int
    large_energy_play_sfx: int
    ammo_per_expansion: int


@dataclasses.dataclass(frozen=True)
class HudUpdateAddresses:
    cloak_base_case: int
    hud_up_cloak_base: int
    hud_up_weapon_unlocked_case_2: int


@dataclasses.dataclass(frozen=True)
class ProcessState:
    octolith_picked_up_conditional: int


@dataclasses.dataclass(frozen=True)
class RoomTransitionEndAddresses:
    door_locking_condition: int


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
class DataSectionAddresses:
    story_save_data: int


@dataclasses.dataclass(frozen=True)
class Overlay2Offsets:
    cloak: int
    affinity_weapon: int


@dataclasses.dataclass(frozen=True)
class Overlay8Offsets:
    octolith_start_movie: int
    octolith_set_game_state: int


@dataclasses.dataclass(frozen=True)
class MetroidHuntersTextFileOffsets:
    main_menu_textbox: int
    credits_end_transmission: int


@dataclasses.dataclass(frozen=True)
class GameVersion:
    id_code: IdCode
    revision: Revision
    description: str
    init_enemy_hunter_spawns_addresses: InitEnemyHunterSpawnsAddresses
    player_pickup_items_addresses: PlayerPickupItemsAddresses
    hud_update_addresses: HudUpdateAddresses
    process_state: ProcessState
    get_hud_string_address: int
    room_transition_end_addresses: RoomTransitionEndAddresses
    init_save_file_addresses: InitSaveFileAddresses
    data_section_addresses: DataSectionAddresses
    overlay2_offsets: Overlay2Offsets
    overlay8_offsets: Overlay8Offsets
    metroidhunters_text_file_offsets: MetroidHuntersTextFileOffsets


ALL_VERSIONS = [
    GameVersion(
        id_code=IdCode.AMHE,
        revision=Revision.REV0,
        description="USA 1.0",
        init_enemy_hunter_spawns_addresses=InitEnemyHunterSpawnsAddresses(
            random_hunter_spawn_first_condition=0x0201598C,
            random_hunter_spawn_game_state=0x02015AF8,
        ),
        player_pickup_items_addresses=PlayerPickupItemsAddresses(
            small_energy_refill_amount=0x02019BD8,
            medium_energy_refill_amount=0x02019B88,
            large_energy_refill_amount=0x02019BE0,
            missile_launcher=0x02019E80,
            nothing=0x0201A23C,
            missiles_per_expansion=0x0201A350,
            small_ammo_refill_amount=0x02019DD4,
            large_ammo_refill_amount=0x02019D74,
            small_energy_play_sfx=0x0201A144,
            large_energy_play_sfx=0x0201A1E4,
            ammo_per_expansion=0x0201A3AC,
        ),
        hud_update_addresses=HudUpdateAddresses(
            cloak_base_case=0x0202D128,
            hud_up_cloak_base=0x0202D594,
            hud_up_weapon_unlocked_case_2=0x0202DAD0,
        ),
        process_state=ProcessState(
            octolith_picked_up_conditional=0x0202E45C,
        ),
        get_hud_string_address=0x0203C3B0,
        room_transition_end_addresses=RoomTransitionEndAddresses(
            door_locking_condition=0x0205331C,
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
        data_section_addresses=DataSectionAddresses(
            story_save_data=0x020E8C50,
        ),
        overlay2_offsets=Overlay2Offsets(
            cloak=0x01E20A,
            affinity_weapon=0x01E212,
        ),
        overlay8_offsets=Overlay8Offsets(
            octolith_start_movie=0x010A8,
            octolith_set_game_state=0x01120,
        ),
        metroidhunters_text_file_offsets=MetroidHuntersTextFileOffsets(
            main_menu_textbox=7944,
            credits_end_transmission=3600,
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
            small_energy_refill_amount=0x02019BD8,
            medium_energy_refill_amount=0x02019B88,
            large_energy_refill_amount=0x02019BE0,
            missile_launcher=0x02019E80,
            nothing=0x0201A23C,
            missiles_per_expansion=0x0201A350,
            small_ammo_refill_amount=0x02019DD4,
            large_ammo_refill_amount=0x02019D74,
            small_energy_play_sfx=0x0201A144,
            large_energy_play_sfx=0x0201A1E4,
            ammo_per_expansion=0x0201A3AC,
        ),
        hud_update_addresses=HudUpdateAddresses(
            cloak_base_case=0x0202D128,
            hud_up_cloak_base=0x0202D594,
            hud_up_weapon_unlocked_case_2=0x0202DAD0,
        ),
        process_state=ProcessState(
            octolith_picked_up_conditional=0x0202E45C,
        ),
        get_hud_string_address=0x0203C2E0,
        room_transition_end_addresses=RoomTransitionEndAddresses(
            door_locking_condition=0x02053B3C,
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
        data_section_addresses=DataSectionAddresses(
            story_save_data=0x020E9710,
        ),
        overlay2_offsets=Overlay2Offsets(
            cloak=0x01E26A,
            affinity_weapon=0x01E272,
        ),
        overlay8_offsets=Overlay8Offsets(
            octolith_start_movie=0x010A8,
            octolith_set_game_state=0x01120,
        ),
        metroidhunters_text_file_offsets=MetroidHuntersTextFileOffsets(
            main_menu_textbox=6792,
            credits_end_transmission=3144,
        ),
    ),
    GameVersion(
        id_code=IdCode.AMHP,
        revision=Revision.REV0,
        description="Europe 1.0",
        init_enemy_hunter_spawns_addresses=InitEnemyHunterSpawnsAddresses(
            random_hunter_spawn_first_condition=0x02015988,
            random_hunter_spawn_game_state=0x02015AF0,
        ),
        player_pickup_items_addresses=PlayerPickupItemsAddresses(
            small_energy_refill_amount=0x02019BD8,
            medium_energy_refill_amount=0x02019B88,
            large_energy_refill_amount=0x02019BE0,
            missile_launcher=0x02019E80,
            nothing=0x0201A23C,
            missiles_per_expansion=0x0201A350,
            small_ammo_refill_amount=0x02019DD4,
            large_ammo_refill_amount=0x02019D74,
            small_energy_play_sfx=0x0201A144,
            large_energy_play_sfx=0x0201A1E4,
            ammo_per_expansion=0x0201A3AC,
        ),
        hud_update_addresses=HudUpdateAddresses(
            cloak_base_case=0x0202D120,
            hud_up_cloak_base=0x0202D58C,
            hud_up_weapon_unlocked_case_2=0x0202DAC8,
        ),
        process_state=ProcessState(
            octolith_picked_up_conditional=0x0202E45C,
        ),
        get_hud_string_address=0x0203C2D8,
        room_transition_end_addresses=RoomTransitionEndAddresses(
            door_locking_condition=0x02053B10,
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
        data_section_addresses=DataSectionAddresses(
            story_save_data=0x020E9730,
        ),
        overlay2_offsets=Overlay2Offsets(
            cloak=0x01E20A,
            affinity_weapon=0x01E212,
        ),
        overlay8_offsets=Overlay8Offsets(
            octolith_start_movie=0x010A8,
            octolith_set_game_state=0x01120,
        ),
        metroidhunters_text_file_offsets=MetroidHuntersTextFileOffsets(
            main_menu_textbox=8012,
            credits_end_transmission=3632,
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
            small_energy_refill_amount=0x02019BD8,
            medium_energy_refill_amount=0x02019B88,
            large_energy_refill_amount=0x02019BE0,
            missile_launcher=0x02019E80,
            nothing=0x0201A23C,
            missiles_per_expansion=0x0201A350,
            small_ammo_refill_amount=0x02019DD4,
            large_ammo_refill_amount=0x02019D74,
            small_energy_play_sfx=0x0201A144,
            large_energy_play_sfx=0x0201A1E4,
            ammo_per_expansion=0x0201A3AC,
        ),
        hud_update_addresses=HudUpdateAddresses(
            cloak_base_case=0x0202D128,
            hud_up_cloak_base=0x0202D594,
            hud_up_weapon_unlocked_case_2=0x0202DAD0,
        ),
        process_state=ProcessState(
            octolith_picked_up_conditional=0x0202E45C,
        ),
        get_hud_string_address=0x0203C2E0,
        room_transition_end_addresses=RoomTransitionEndAddresses(
            door_locking_condition=0x02053B3C,
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
        data_section_addresses=DataSectionAddresses(
            story_save_data=0x020E97B0,
        ),
        overlay2_offsets=Overlay2Offsets(
            cloak=0x01E26A,
            affinity_weapon=0x01E272,
        ),
        overlay8_offsets=Overlay8Offsets(
            octolith_start_movie=0x010A8,
            octolith_set_game_state=0x01120,
        ),
        metroidhunters_text_file_offsets=MetroidHuntersTextFileOffsets(
            main_menu_textbox=6792,
            credits_end_transmission=3144,
        ),
    ),
    GameVersion(
        id_code=IdCode.AMHJ,
        revision=Revision.REV0,
        description="Japanese 1.0",
        init_enemy_hunter_spawns_addresses=InitEnemyHunterSpawnsAddresses(
            random_hunter_spawn_first_condition=0x02015984,
            random_hunter_spawn_game_state=0x02015AD8,
        ),
        player_pickup_items_addresses=PlayerPickupItemsAddresses(
            small_energy_refill_amount=0x02019BD8,
            medium_energy_refill_amount=0x02019B88,
            large_energy_refill_amount=0x02019BE0,
            missile_launcher=0x02019E80,
            nothing=0x0201A23C,
            missiles_per_expansion=0x0201A350,
            small_ammo_refill_amount=0x02019DD4,
            large_ammo_refill_amount=0x02019D74,
            small_energy_play_sfx=0x0201A144,
            large_energy_play_sfx=0x0201A1E4,
            ammo_per_expansion=0x0201A3AC,
        ),
        hud_update_addresses=HudUpdateAddresses(
            cloak_base_case=0x0202D128,
            hud_up_cloak_base=0x0202D594,
            hud_up_weapon_unlocked_case_2=0x0202DAD0,
        ),
        process_state=ProcessState(
            octolith_picked_up_conditional=0x0202E45C,
        ),
        get_hud_string_address=0x0203C2E0,
        room_transition_end_addresses=RoomTransitionEndAddresses(
            door_locking_condition=0x02054D6C,
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
        data_section_addresses=DataSectionAddresses(
            story_save_data=0x020EADA0,
        ),
        overlay2_offsets=Overlay2Offsets(
            cloak=0x01E20A,
            affinity_weapon=0x01E212,
        ),
        overlay8_offsets=Overlay8Offsets(
            octolith_start_movie=0x010A8,
            octolith_set_game_state=0x01120,
        ),
        metroidhunters_text_file_offsets=MetroidHuntersTextFileOffsets(
            main_menu_textbox=7944,
            credits_end_transmission=3600,
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
