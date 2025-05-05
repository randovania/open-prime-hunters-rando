import copy
import enum
import math
import typing
from collections.abc import Collection, Iterator
from typing import Any, Self

import construct
from construct import (
    Aligned,
    BitsSwapped,
    Bitwise,
    Byte,
    Container,
    Flag,
    Int16sl,
    Int16ul,
    Int32sl,
    Int32ul,
    ListContainer,
    Padded,
    PaddedString,
    Peek,
    Pointer,
    Rebuild,
    RepeatUntil,
    StopIf,
    Struct,
    Switch,
    this,
)

from open_prime_hunters_rando.constants import EnumAdapter


class EntityType(enum.Enum):
    PLATFORM = 0
    OBJECT = 1
    PLAYER_SPAWN = 2
    DOOR = 3
    ITEM_SPAWN = 4
    ENEMY_SPAWN = 6
    TRIGGER_VOLUME = 7
    AREA_VOLUME = 8
    JUMP_PAD = 9
    POINT_MODULE = 10  # unused
    MORPH_CAMERA = 11
    OCTOLITH_FLAG = 12
    FLAG_BASE = 13
    TELEPORTER = 14
    DEFENSE_NODE = 15
    LIGHT_SOURCE = 16
    ARTIFACT = 17
    CAMERA_SEQUENCE = 18
    FORCE_FIELD = 19


EntityTypeConstruct = EnumAdapter(EntityType, Int16ul)


class FixedAdapter(construct.Adapter):
    """Fixed-point number with 12-bit fractional part"""

    def __init__(self) -> None:
        super().__init__(construct.Int32sl)

    def _decode(self, obj: int, context: dict, path: str) -> float:
        return float(obj) / 4096

    def _encode(self, obj: float, context: dict, path: str) -> int:
        return math.floor(obj * 4096)


Fixed = FixedAdapter()

Vector3Fx = Struct(
    "x" / Fixed,
    "y" / Fixed,
    "z" / Fixed,
)

Vector4Fx = Struct(
    "x" / Fixed,
    "y" / Fixed,
    "z" / Fixed,
    "w" / Fixed,
)

DecodedString = PaddedString(16, "ascii")

EntityDataHeader = Struct(
    "entity_type" / EntityTypeConstruct,
    "entity_id" / Int16sl,
    "position" / Vector3Fx,
    "up_vector" / Vector3Fx,
    "facing_vector" / Vector3Fx,
)


class Message(enum.Enum):
    NONE = 0
    SET_ACTIVE = 5
    DESTROYED = 6
    DAMAGE = 7
    TRIGGER = 9
    UPDATE_MUSIC = 12
    GRAVITY = 15
    UNLOCK = 16
    LOCK = 17
    ACTIVATE = 18
    COMPLETE = 19
    IMPACT = 20
    DEATH = 21
    UNUSED_22 = 22
    SHIP_HATCH = 23
    UNUSED_24 = 24
    UNUSED_25 = 25
    SHOW_PROMPT = 26
    SHOW_WARNING = 27
    SHOW_OVERLAY = 28
    MOVE_ITEM_SPAWNER = 29
    SET_CAM_SEQ_AI = 30
    PLAYER_COLLIDE_WITH = 31
    BEAM_COLLIDE_WITH = 32
    UNLOCK_CONNECTORS = 33
    LOCK_CONNECTORS = 34
    PREVENT_FORM_SWITCH = 35
    UNKNOWN_36 = 36
    SET_TRIGGER_STATE = 42
    CLEAR_TRIGGER_STATE = 43
    PLATFORM_WAKEUP = 44
    PLATFORM_SLEEP = 45
    DRIP_MOAT_PLATFORM = 46
    ACTIVATE_TURRET = 48
    DECREASE_TURRET_LIGHTS = 49
    INCREASE_TURRET_LIGHTS = 50
    DEACTIVATE_TURRET = 51
    SET_BEAM_REFLECTION = 52
    SET_PLATFORM_INDEX = 53
    PLAY_SFX_SCRIPT = 54
    UNLOCK_OUBLIETTE = 56
    CHECKPOINT = 57
    ESCAPE_UPDATE1 = 58
    SET_SEEK_PLAYER_Y = 59
    LOAD_OUBLIETTE = 60
    ESCAPE_UPDATE2 = 61


MessageConstruct = EnumAdapter(Message, Int32ul)


class PlatformFlags(enum.IntFlag):
    NONE = 0x0
    HAZARD = 0x1
    CONTACT_DAMAGE = 0x2
    BEAM_SPAWNER = 0x4
    BEAM_COL_EFFECT = 0x8
    DAMAGE_REFLECT1 = 0x10
    DAMAGE_REFLECT2 = 0x20
    STANDING_COL_ONLY = 0x40
    START_SLEEP = 0x80
    SLEEP_AT_END = 0x100
    DRIP_MOAT = 0x200
    SKIP_NODE_REF = 0x400
    DRAW_IF_NODE_REF = 0x800
    DRAW_ALWAYS = 0x1000
    HIDE_ON_SLEEP = 0x2000
    SYLUX_SHIP = 0x4000
    BIT15 = 0x8000
    BEAM_REFLECTION = 0x10000
    USE_ROOM_STATE = 0x20000
    BEAM_TARGET = 0x40000
    SAMUS_SHIP = 0x80000
    BREAKABLE = 0x100000
    PERSIST_ROOM_STATE = 0x200000
    NO_BEAM_IF_CULL = 0x400000
    NO_RECOIL = 0x800000
    BIT24 = 0x1000000
    BIT25 = 0x2000000
    BIT26 = 0x4000000
    BIT27 = 0x8000000
    BIT28 = 0x10000000
    BIT29 = 0x20000000
    BIT30 = 0x40000000
    BIT31 = 0x80000000


class ItemType(enum.Enum):
    NONE = -1
    HEALTH_MEDIUM = 0
    HEALTH_SMALL = 1
    HEALTH_BIG = 2
    DOUBLE_DAMAGE = 3
    ENERGY_TANK = 4
    VOLT_DRIVER = 5
    MISSILE_EXPANSION = 6
    BATTLEHAMMER = 7
    IMPERIALIST = 8
    JUDICATOR = 9
    MAGMAUL = 10
    SHOCK_COIL = 11
    OMEGA_CANNON = 12
    UA_SMALL = 13
    UA_BIG = 14
    MISSILE_SMALL = 15
    MISSILE_BIG = 16
    CLOAK = 17
    UA_EXPANSION = 18
    ARTIFACT_KEY = 19
    DEATHALT = 20
    AFFINITY_WEAPON = 21
    PICK_WPN_MISSILE = 22


ItemTypeConstruct = EnumAdapter(ItemType, Int32sl)

PlatformEntityData = Struct(
    "header" / EntityDataHeader,
    "no_port" / Int32ul,
    "model_id" / Int32ul,
    "parent_id" / Int16sl,
    "active" / Flag,
    "delay" / Byte,
    "scan_data1" / Int16ul,
    "scan_message_target" / Int16sl,
    "scan_message" / MessageConstruct,
    "scan_data2" / Int16ul,
    "position_count" / Int16ul,
    "positions" / Vector3Fx[10],
    "rotations" / Vector4Fx[10],
    "position_offset" / Vector3Fx,
    "forward_speed" / Fixed,
    "backward_speed" / Fixed,
    "portal_name" / DecodedString,
    "movement_type" / Int32ul,
    "for_cutscene" / Int32ul,
    "reverse_type" / Int32ul,
    "flags" / construct.FlagsEnum(Int32ul, PlatformFlags),
    "contact_damage" / Int32ul,
    "beam_spawn_direction" / Vector3Fx,
    "beam_spawn_position" / Vector3Fx,
    "beam_id" / Int32sl,
    "beam_interval" / Int32ul,
    "beam_on_intervals" / Int32ul,
    "_unused1" / Int16ul,
    "_unused2" / Int16ul,
    "resist_effect_id" / Int32sl,
    "health" / Int32ul,
    "effectiveness" / Int32ul,
    "damage_effect_id" / Int32sl,
    "dead_effect_id" / Int32sl,
    "item_chance" / Byte,
    "_padding1" / Byte,
    "_padding2" / Int16ul,
    "item_type" / ItemTypeConstruct,
    "_unused3" / Int32ul,
    "_unused4" / Int32ul,
    "beam_hit_message_target" / Int32sl,
    "beam_hit_message" / MessageConstruct,
    "beam_hit_message_param1" / Int32sl,
    "beam_hit_message_param2" / Int32sl,
    "player_collision_message_target" / Int32sl,
    "player_collision_message" / MessageConstruct,
    "player_collision_message_param1" / Int32sl,
    "player_collision_message_param2" / Int32sl,
    "dead_message_target" / Int32sl,
    "dead_message" / MessageConstruct,
    "dead_message_param1" / Int32sl,
    "dead_message_param2" / Int32sl,
    "lifetime_message1_index" / Int16ul,
    "lifetime_message1_target" / Int16sl,
    "lifetime_message1" / MessageConstruct,
    "lifetime_message1_param1" / Int32sl,
    "lifetime_message1_param2" / Int32sl,
    "lifetime_message2_index" / Int16ul,
    "lifetime_message2_target" / Int16sl,
    "lifetime_message2" / MessageConstruct,
    "lifetime_message2_param1" / Int32sl,
    "lifetime_message2_param2" / Int32sl,
    "lifetime_message3_index" / Int16ul,
    "lifetime_message3_target" / Int16sl,
    "lifetime_message3" / MessageConstruct,
    "lifetime_message3_param1" / Int32sl,
    "lifetime_message3_param2" / Int32sl,
    "lifetime_message4_index" / Int16ul,
    "lifetime_message4_target" / Int16sl,
    "lifetime_message4" / MessageConstruct,
    "lifetime_message4_param1" / Int32sl,
    "lifetime_message4_param2" / Int32sl,
)


class ObjectFlags(enum.IntFlag):
    NONE = 0x0
    STATE_BIT0 = 0x1
    STATE_BIT1 = 0x2
    STATE = 0x3
    NO_ANIMATION = 0x4
    ENTITY_LINKED = 0x8
    IS_VISIBLE = 0x10


class ObjectEffectFlags(enum.IntFlag):
    NONE = 0x0
    USE_EFFECT_VOLUME = 0x1
    USE_EFFECT_OFFSET = 0x2
    REPEAT_SCAN_MESSAGE = 0x4
    WEAPON_ZOOM = 0x8
    ATTACH_EFFECT = 0x10
    DESTROY_EFFECT = 0x20
    ALWAYS_UPDATE_EFFECT = 0x40
    UNKNOWN = 0x8000


class VolumeType(enum.Enum):
    BOX = 0
    CYLINDER = 1
    SPHERE = 2


volume_types = {
    VolumeType.BOX: Struct(
        "box_vector1" / Vector3Fx,
        "box_vector2" / Vector3Fx,
        "box_vector3" / Vector3Fx,
        "box_position" / Vector3Fx,
        "box_dot1" / Fixed,
        "box_dot2" / Fixed,
        "box_dot3" / Fixed,
    ),
    VolumeType.CYLINDER: Struct(
        "cylinder_vector" / Vector3Fx,
        "cylinder_position" / Vector3Fx,
        "cylinder_radius" / Fixed,
        "cylinder_dot" / Fixed,
    ),
    VolumeType.SPHERE: Struct(
        "sphere_position" / Vector3Fx,
        "sphere_radius" / Fixed,
    ),
}

RawCollisionVolume = Struct(
    "type" / EnumAdapter(VolumeType, Int32ul),
    "data" / Padded(60, Switch(construct.this.type, volume_types)),
)

ObjectEntityData = Struct(
    "header" / EntityDataHeader,
    "flags" / construct.FlagsEnum(Byte, ObjectFlags),
    "_padding1" / Byte,
    "_padding2" / Int16ul,
    "effect_flags" / construct.FlagsEnum(Int32ul, ObjectEffectFlags),
    "model_id" / Int32sl,
    "linked_entity" / Int16sl,
    "scan_id" / Int16ul,
    "scan_message_target" / Int16sl,
    "_padding3" / Int16ul,
    "scan_message" / MessageConstruct,
    "effect_id" / Int32sl,
    "effect_interval" / Int32ul,
    "effect_on_inverals" / Int32ul,
    "effect_position_offset" / Vector3Fx,
    "volume" / RawCollisionVolume,
)

PlayerSpawnEntityData = Struct(
    "header" / EntityDataHeader,
    "availability" / Byte,
    "active" / Byte,
    "team_index" / Byte,
)


class DoorType(enum.Enum):
    STANDARD = 0
    MORPH_BALL = 1
    BOSS = 2
    THIN = 3


class PaletteId(enum.Enum):
    POWER_BEAM = 0
    VOLT_DRIVER = 1
    MISSILE = 2
    BATTLEHAMMER = 3
    IMPERIALIST = 4
    JUDICATOR = 5
    MAGMAUL = 6
    SHOCK_COIL = 7
    OMEGA_CANNON = 8
    LOCKED = 9


PaletteIdConstruct = EnumAdapter(PaletteId, Int32ul)

DoorEntityData = Struct(
    "header" / EntityDataHeader,
    "node_name" / DecodedString,
    "palette_id" / PaletteIdConstruct,
    "door_type" / EnumAdapter(DoorType, Int32ul),
    "connector_id" / Int32ul,
    "target_layer_id" / Byte,
    "locked" / Flag,
    "out_connector_id" / Byte,
    "out_loader_id" / Byte,
    "entity_file_name" / DecodedString,
    "room_name" / DecodedString,
)


ItemSpawnEntityData = Struct(
    "header" / EntityDataHeader,
    "parent_id" / Int32sl,
    "item_type" / ItemTypeConstruct,
    "enabled" / Flag,
    "has_base" / Flag,
    "always_active" / Flag,
    "_padding" / Byte,
    "max_spawn_count" / Int16ul,
    "spawn_interval" / Int16ul,
    "spawn_delay" / Int16ul,
    "notify_entity_id" / Int16sl,
    "collected_message" / MessageConstruct,
    "collected_message_param1" / Int32ul,
    "collected_message_param2" / Int32ul,
)


class EnemyType(enum.Enum):
    WAR_WASP = 0
    ZOOMER = 1
    TEMROID = 2
    PETRASYL1 = 3
    PETRASYL2 = 4
    PETRASYL3 = 5
    PETRASYL4 = 6
    UNKNOWN_7 = 7  # unused
    UNKNOWN_8 = 8  # unused
    UNKNOWN_9 = 9  # unused
    BARBED_WAR_WASP = 10
    SHRIEKBAT = 11
    GEEMER = 12
    UNKNOWN_13 = 13  # unused
    UNKNOWN_14 = 14  # unused
    UNKNOWN_15 = 15  # unused
    BLASTCAP = 16
    UNKNOWN_17 = 17  # unused
    ALIMBIC_TURRET = 18
    CRETAPHID = 19
    CRETAPHID_EYE = 20
    CRETAPHID_CRYSTAL = 21
    UNKNOWN_22 = 22  # unused (Cretaphid-related)
    PSYCHO_BIT1 = 23
    GOREA1_A = 24
    GOREA_HEAD = 25
    GOREA_ARM = 26
    GOREA_LEG = 27
    GOREA1_B = 28
    GOREA_SEAL_SPHERE1 = 29
    TROCRA = 30
    GOREA2 = 31
    GOREA_SEAL_SPHERE2 = 32
    GOREA_METEOR = 33
    PSYCHO_BIT2 = 34  # unused
    VOLDRUM2 = 35
    VOLDRUM1 = 36
    QUADTROID = 37
    CRASH_PILLAR = 38
    FIRE_SPAWN = 39
    SPAWNER = 40
    SLENCH = 41
    SLENCH_SHIELD = 42
    SLENCH_NEST = 43
    SLENCH_SYNAPSE = 44
    SLENCH_TURRET = 45
    LESSER_ITHRAK = 46
    GREATER_ITHRAK = 47
    HUNTER = 48
    FORCE_FIELD_LOCK = 49
    HIT_ZONE = 50  # used by 39/46/47
    CARNIVOROUS_PLANT = 51


EnemyTypeConstruct = EnumAdapter(EnemyType, Byte)


class Hunter(enum.Enum):
    SAMUS = 0
    KANDEN = 1
    TRACE = 2
    SYLUX = 3
    NOXUS = 4
    SPIRE = 5
    WEAVEL = 6
    GUARDIAN = 7
    RANDOM = 8


HunterConstruct = EnumAdapter(Hunter, Int32ul)


WarWaspSpawnField = Struct(
    "volume0" / RawCollisionVolume,
    "volume1" / RawCollisionVolume,
    "volume2" / RawCollisionVolume,
    "movement_vectors" / Vector3Fx[16],
    "position_count" / Byte,
    "_padding1" / Byte,
    "_padding2" / Int16ul,
    "movement_type" / Int32ul,
)


EnemySpawnField0 = Struct(
    "volume0" / RawCollisionVolume,
    "volume1" / RawCollisionVolume,
    "volume2" / RawCollisionVolume,
    "volume3" / RawCollisionVolume,
)
EnemySpawnField1 = Struct(
    "war_wasp" / WarWaspSpawnField,
    "_padding1" / Int16ul,
    "_padding2" / Int16ul,
)
EnemySpawnField2 = Struct(
    "volume0" / RawCollisionVolume,
    "path_vector" / Vector3Fx,
    "volume1" / RawCollisionVolume,
    "volume2" / RawCollisionVolume,
)
EnemySpawnField3 = Struct(
    "volume0" / RawCollisionVolume,
    "_unused" / Int32ul[7],
    "facing" / Vector3Fx,
    "position" / Vector3Fx,
    "idle_range" / Vector3Fx,
)
EnemySpawnField4 = Struct(
    "volume0" / RawCollisionVolume,
    "_unused" / Int32ul[4],
    "position" / Vector3Fx,
    "weave_offset" / Int32ul,
    "field" / Int32sl,
)
EnemySpawnField5 = Struct(
    "enemy_subtype" / Int32ul,
    "volume0" / RawCollisionVolume,
    "volume1" / RawCollisionVolume,
    "volume2" / RawCollisionVolume,
    "volume3" / RawCollisionVolume,
)
EnemySpawnField6 = Struct(
    "enemy_subtype" / Int32ul,
    "enemy_version" / Int32ul,
    "volume0" / RawCollisionVolume,
    "volume1" / RawCollisionVolume,
    "volume2" / RawCollisionVolume,
    "volume3" / RawCollisionVolume,
)
EnemySpawnField7 = Struct(
    "enemy_health" / Int16ul,
    "enemy_damage" / Int16ul,
    "enemy_subtype" / Int32ul,
    "volume0" / RawCollisionVolume,
)
EnemySpawnField8 = Struct(
    "enemy_subtype" / Int32ul,
    "enemy_version" / Int32ul,
    "war_wasp" / WarWaspSpawnField,
)
EnemySpawnField9 = Struct(
    "hunter_id" / HunterConstruct,
    "encounter_type" / Int32ul,
    "hunter_weapon" / Int32ul,
    "hunter_health" / Int16ul,
    "hunter_health_max" / Int16ul,
    "field" / Int16ul,  # set in AI data
    "hunter_color" / Byte,
    "hunter_chance" / Byte,
)
EnemySpawnField10 = Struct(
    "enemy_subtype" / Int32ul,
    "enemy_version" / Int32ul,
    "volume0" / RawCollisionVolume,
    "volume1" / RawCollisionVolume,
    "index" / Int32sl,
)
EnemySpawnField11 = Struct(
    "sphere1_position" / Vector3Fx,
    "sphere1_radius" / Fixed,
    "sphere2_position" / Vector3Fx,
    "sphere2_radius" / Fixed,
)
EnemySpawnField12 = Struct(
    "field1" / Vector3Fx,
    "field2" / Int32ul,
    "field3" / Int32ul,
)


enemy_to_spawn_field = {
    EnemyType.ZOOMER: EnemySpawnField0,
    EnemyType.GEEMER: EnemySpawnField0,
    EnemyType.BLASTCAP: EnemySpawnField0,
    EnemyType.QUADTROID: EnemySpawnField0,
    EnemyType.CRASH_PILLAR: EnemySpawnField0,
    EnemyType.SLENCH: EnemySpawnField0,
    EnemyType.LESSER_ITHRAK: EnemySpawnField0,
    EnemyType.TROCRA: EnemySpawnField0,
    EnemyType.VOLDRUM2: EnemySpawnField0,
    EnemyType.WAR_WASP: EnemySpawnField1,
    EnemyType.SHRIEKBAT: EnemySpawnField2,
    EnemyType.TEMROID: EnemySpawnField3,
    EnemyType.PETRASYL1: EnemySpawnField3,
    EnemyType.PETRASYL2: EnemySpawnField4,
    EnemyType.PETRASYL3: EnemySpawnField4,
    EnemyType.PETRASYL4: EnemySpawnField4,
    EnemyType.CRETAPHID: EnemySpawnField5,
    EnemyType.GREATER_ITHRAK: EnemySpawnField5,
    EnemyType.ALIMBIC_TURRET: EnemySpawnField6,
    EnemyType.PSYCHO_BIT1: EnemySpawnField6,
    EnemyType.PSYCHO_BIT2: EnemySpawnField6,
    EnemyType.VOLDRUM1: EnemySpawnField6,
    EnemyType.FIRE_SPAWN: EnemySpawnField6,
    EnemyType.CARNIVOROUS_PLANT: EnemySpawnField7,
    EnemyType.BARBED_WAR_WASP: EnemySpawnField8,
    EnemyType.HUNTER: EnemySpawnField9,
    EnemyType.SLENCH_TURRET: EnemySpawnField10,
    EnemyType.GOREA1_A: EnemySpawnField11,
    EnemyType.GOREA2: EnemySpawnField12,
}


EnemySpawnEntityData = Struct(
    "header" / EntityDataHeader,
    "enemy_type" / EnemyTypeConstruct,
    "_padding1" / Byte,
    "_padding2" / Int16ul,
    "fields" / Padded(400, Switch(construct.this.enemy_type, enemy_to_spawn_field)),
    "linked_entity_id" / Int16sl,
    "spawn_limit" / Byte,
    "spawn_total" / Byte,
    "spawn_count" / Byte,
    "active" / Flag,
    "always_active" / Flag,
    "item_chance" / Byte,
    "spawner_health" / Int16ul,
    "cooldown_time" / Int16ul,
    "initial_cooldown" / Int16ul,
    "_padding3" / Int16ul,
    "active_distance" / Fixed,
    "enemy_active_distance" / Fixed,
    "node_name" / DecodedString,
    "entity_id1" / Int16sl,
    "_padding4" / Int16ul,
    "message1" / MessageConstruct,
    "entity_id2" / Int16sl,
    "_padding5" / Int16ul,
    "message2" / MessageConstruct,
    "entity_id3" / Int16sl,
    "_padding6" / Int16ul,
    "message3" / MessageConstruct,
    "item_type" / ItemTypeConstruct,
)


class TriggerVolumeType(enum.Enum):
    VOLUME = 0
    THRESHOLD = 1
    RELAY = 2
    AUTOMATIC = 3
    STATE_BITS = 4


class TriggerVolumeFlags(enum.IntFlag):
    NONE = 0x0
    POWER_BEAM = 0x1
    VOLT_DRIVER = 0x2
    MISSILE = 0x4
    BATTLEHAMMER = 0x8
    IMPERIALIST = 0x10
    JUDICATOR = 0x20
    MAGMAUL = 0x40
    SHOCK_COIL = 0x80
    BEAM_CHARGED = 0x100
    PLAYER_BIPED = 0x200
    PLAYER_ALT = 0x400
    BIT_11 = 0x800  # unused
    INCLUDE_BOTS = 0x1000


TriggerVolumeFlagsConstruct = construct.FlagsEnum(Int32ul, TriggerVolumeFlags)

TriggerVolumeEntityData = Struct(
    "header" / EntityDataHeader,
    "subtype" / EnumAdapter(TriggerVolumeType, Int32ul),
    "volume" / RawCollisionVolume,
    "_unused" / Int16ul,
    "active" / Flag,
    "always_active" / Flag,
    "deactivate_after_use" / Flag,
    "_padding1" / Byte,
    "repeat_delay" / Int16ul,
    "check_delay" / Int16ul,
    "required_state_bit" / Int16ul,
    "trigger_flags" / TriggerVolumeFlagsConstruct,
    "trigger_threshold" / Int32ul,
    "parent_id" / Int16sl,
    "_padding2" / Int16ul,
    "parent_message" / MessageConstruct,
    "parent_message_param1" / Int32sl,
    "parent_message_param2" / Int32sl,
    "child_id" / Int16sl,
    "_padding3" / Int16ul,
    "child_message" / MessageConstruct,
    "child_message_param1" / Int32sl,
    "child_message_param2" / Int32sl,
)


AreaVolumeEntityData = Struct(
    "header" / EntityDataHeader,
    "volume" / RawCollisionVolume,
    "_unused1" / Int16ul,
    "active" / Flag,
    "always_active" / Flag,
    "allow_mulitple" / Flag,
    "message_delay" / Byte,
    "_unused2" / Int16ul,
    "inside_message" / MessageConstruct,
    "inside_message_param1" / Int32sl,
    "inside_message_param2" / Int32sl,
    "parent_id" / Int16sl,
    "_padding3" / Int16ul,
    "exit_message" / MessageConstruct,
    "exit_message_param1" / Int32sl,
    "exit_message_param2" / Int32sl,
    "child_id" / Int16sl,
    "cooldown" / Int16ul,
    "priority" / Int32ul,
    "trigger_flags" / TriggerVolumeFlagsConstruct,
)

JumpPadEntityData = Struct(
    "header" / EntityDataHeader,
    "parent_id" / Int32sl,
    "_unused" / Int32ul,
    "volume" / RawCollisionVolume,
    "beam_vector" / Vector3Fx,
    "speed" / Fixed,
    "control_lock_time" / Int16ul,
    "cooldown_time" / Int16ul,
    "active" / Flag,
    "_padding1" / Byte,
    "_padding2" / Int16ul,
    "model_id" / Int32ul,
    "beam_type" / Int32ul,
    "trigger_flags" / TriggerVolumeFlagsConstruct,
)

PointModuleEntityData = Struct(
    "header" / EntityDataHeader,
    "next_id" / Int16sl,
    "prev_id" / Int16sl,
    "active" / Flag,
)

MorphCameraEntityData = Struct(
    "header" / EntityDataHeader,
    "volume" / RawCollisionVolume,
)

OctolithFlagEntityData = Struct(
    "header" / EntityDataHeader,
    "team_id" / Byte,
)

FlagBaseEntityData = Struct(
    "header" / EntityDataHeader,
    "team_id" / Int32ul,
    "volume" / RawCollisionVolume,
)

TeleporterEntityData = Struct(
    "header" / EntityDataHeader,
    "load_index" / Byte,
    "target_index" / Byte,
    "artifact_id" / Byte,
    "active" / Flag,
    "invisible" / Flag,
    "entity_filename" / PaddedString(15, "ascii"),
    "_unused" / Int16ul[2],
    "target_position" / Vector3Fx,
    "node_name" / DecodedString,
)

DefenseNodeEntityData = Struct(
    "header" / EntityDataHeader,
    "volume" / RawCollisionVolume,
)


class ColorRgbAdapter(construct.Adapter):
    """RGB for LightSource Entities"""

    def __init__(self) -> None:
        super().__init__(construct.Byte)

    def _decode(self, obj: int, context: dict, path: str) -> float:
        return float(obj) / 255

    def _encode(self, obj: float, context: dict, path: str) -> int:
        return math.floor(obj * 255)


ColorRgb = Struct(
    "red" / ColorRgbAdapter(),
    "green" / ColorRgbAdapter(),
    "blue" / ColorRgbAdapter(),
)

LightSourceEntityData = Struct(
    "header" / EntityDataHeader,
    "volume" / RawCollisionVolume,
    "light1_enabled" / Flag,
    "light1_color" / ColorRgb,
    "light1_vector" / Vector3Fx,
    "light2_enabled" / Flag,
    "light2_color" / ColorRgb,
    "light2_vector" / Vector3Fx,
)

ArtifactEntityData = Struct(
    "header" / EntityDataHeader,
    "model_id" / Byte,
    "artifact_id" / Byte,
    "active" / Flag,
    "has_base" / Flag,
    "message1_target" / Int16sl,
    "_padding1" / Int16ul,
    "message1" / MessageConstruct,
    "message2_target" / Int16sl,
    "_padding2" / Int16ul,
    "message2" / MessageConstruct,
    "message3_target" / Int16sl,
    "_padding3" / Int16ul,
    "message3" / MessageConstruct,
    "linked_entity_id" / Int16sl,
)

CameraSequenceEntityData = Struct(
    "header" / EntityDataHeader,
    "sequence_id" / Byte,
    "handoff" / Flag,
    "loop" / Flag,
    "block_input" / Flag,
    "force_alt_form" / Flag,
    "force_biped_form" / Flag,
    "delay_frames" / Int16ul,
    "player_id1" / Byte,
    "player_id2" / Byte,
    "entity1" / Int16sl,
    "entity2" / Int16sl,
    "end_message_target_id" / Int16sl,
    "end_message" / MessageConstruct,
    "end_message_param" / Int32sl,
)

ForceFieldEntityData = Struct(
    "header" / EntityDataHeader,
    "type" / PaletteIdConstruct,
    "width" / Fixed,
    "height" / Fixed,
    "active" / Flag,
)

types_to_construct = {
    EntityType.PLATFORM: PlatformEntityData,
    EntityType.OBJECT: ObjectEntityData,
    EntityType.PLAYER_SPAWN: PlayerSpawnEntityData,
    EntityType.DOOR: DoorEntityData,
    EntityType.ITEM_SPAWN: ItemSpawnEntityData,
    EntityType.ENEMY_SPAWN: EnemySpawnEntityData,
    EntityType.TRIGGER_VOLUME: TriggerVolumeEntityData,
    EntityType.AREA_VOLUME: AreaVolumeEntityData,
    EntityType.JUMP_PAD: JumpPadEntityData,
    EntityType.POINT_MODULE: PointModuleEntityData,
    EntityType.MORPH_CAMERA: MorphCameraEntityData,
    EntityType.OCTOLITH_FLAG: OctolithFlagEntityData,
    EntityType.FLAG_BASE: FlagBaseEntityData,
    EntityType.TELEPORTER: TeleporterEntityData,
    EntityType.DEFENSE_NODE: DefenseNodeEntityData,
    EntityType.LIGHT_SOURCE: LightSourceEntityData,
    EntityType.ARTIFACT: ArtifactEntityData,
    EntityType.CAMERA_SEQUENCE: CameraSequenceEntityData,
    EntityType.FORCE_FIELD: ForceFieldEntityData,
}

raw_entry_fields = [
    "node_name" / DecodedString,
    "layer_state" / BitsSwapped(Bitwise(Flag[16])),
    "_size" / Int16ul,
    "_data_offset" / Int32ul,
]

RawEntityEntry = Struct(*raw_entry_fields)

EntityEntry = Struct(
    *raw_entry_fields,
    StopIf(this._data_offset == 0),
    "_entity_type" / Rebuild(Peek(Pointer(this._data_offset, EntityTypeConstruct)), this.data.header.entity_type),
    "data" / Pointer(this._data_offset, Aligned(4, Switch(this._entity_type, types_to_construct))),
)

EntityFileHeader = Struct(
    "version" / Int32ul,
    "layer_counts" / Int16ul[16],
)

EntityFileConstruct = Struct(
    "header" / EntityFileHeader,
    "entities" / RepeatUntil(lambda entity, lst, ctx: entity._data_offset == 0, EntityEntry),
)


def num_bytes_to_align(length: int, modulus: int = 4) -> int:
    if length % modulus > 0:
        return modulus - (length % modulus)
    return 0


class EntityAdapter(construct.Adapter):
    def __init__(self) -> None:
        super().__init__(EntityFileConstruct)

    def _decode(self, obj: Container, context: Container, path: str) -> Container:
        decoded = copy.deepcopy(obj)

        # remove empty entry
        decoded.entities.pop()

        # wrap entities
        decoded.entities = ListContainer([Entity(entity) for entity in decoded.entities])

        return decoded

    def _encode(self, obj: Container, context: Container, path: str) -> Container:
        encoded = copy.deepcopy(obj)

        entities = typing.cast("list[Entity]", encoded.entities)

        # update sizes and offsets
        encoded.entities = ListContainer()

        offset = EntityFileHeader.sizeof()
        offset += RawEntityEntry.sizeof() * (len(entities) + 1)

        for entity_wrapper in entities:
            entity = entity_wrapper._raw

            size = entity_wrapper.size
            entity._size = size
            entity._data_offset = offset

            offset += size + num_bytes_to_align(size)

            encoded.entities.append(entity)

        # add empty entry
        encoded.entities.append(
            Container(
                {
                    "node_name": "",
                    "layer_state": [False] * 16,
                    "_size": 0,
                    "_data_offset": 0,
                }
            )
        )

        return encoded


class Entity:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @classmethod
    def create(
        cls, data: Container, node_name: str = "rmMain", active_layers: Collection[int] = tuple(range(16))
    ) -> Self:
        layer_state = [False] * 16
        for layer in active_layers:
            layer_state[layer] = False

        return cls(
            Container(
                {
                    "node_name": node_name,
                    "layer_state": ListContainer(layer_state),
                    "data": data,
                }
            )
        )

    def __repr__(self) -> str:
        return f"<Entity type={self.entity_type} id={self.entity_id}>"

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, Entity):
            return False
        if value.node_name != self.node_name:
            return False
        for i in range(16):
            if value.layer_state(i) != self.layer_state(i):
                return False

        def check_container(container: dict, other: dict) -> bool:
            for k in container.keys() | other.keys():
                if k.startswith("_"):
                    continue
                if isinstance(container[k], dict):
                    if not isinstance(other[k], dict):
                        return False
                    if not check_container(container[k], other[k]):
                        return False
                else:
                    if container[k] != other[k]:
                        return False
            return True

        return check_container(self._raw, value._raw)

    @property
    def node_name(self) -> str:
        return self._raw.node_name

    @node_name.setter
    def node_name(self, value: str) -> None:
        self._raw.node_name = value

    @property
    def active_layers(self) -> tuple[int, ...]:
        return tuple(i for i in range(16) if self.layer_state(i))

    def layer_state(self, layer: int) -> bool:
        return self._raw.layer_state[layer]

    def set_layer_state(self, layer: int, state: bool) -> None:
        self._raw.layer_state[layer] = state

    @property
    def entity_type(self) -> EntityType:
        return self.data.header.entity_type

    @entity_type.setter
    def entity_type(self, value: EntityType) -> None:
        self.data.header.entity_type = value

    @property
    def entity_id(self) -> int:
        return self.data.header.entity_id

    @property
    def data(self) -> Container:
        return self._raw.data

    @data.setter
    def data(self, value: Container) -> None:
        self._raw.data = value

    @property
    def type_construct(self) -> Struct:
        return types_to_construct[self.entity_type]

    @property
    def size(self) -> int:
        return self.type_construct.sizeof()


class EntityFile:
    def __init__(self, raw: Container):
        self._raw = raw

    @classmethod
    def parse(cls, data: bytes) -> Self:
        # align data to 4
        data = bytes(data) + b"\0" * num_bytes_to_align(len(data))

        return cls(EntityAdapter().parse(data))

    def build(self) -> bytes:
        # update layer counts
        for i in range(16):
            self._raw.header.layer_counts[i] = len(list(self.entities_for_layer(i)))

        # build
        data = EntityAdapter().build(self._raw)

        # remove unnecessary alignment bytes
        if self.entities:
            to_strip = num_bytes_to_align(self.entities[-1].size)
            if to_strip:
                data = data[:-to_strip]

        return data

    def __eq__(self, value: Any) -> bool:
        return isinstance(value, EntityFile) and self.version == value.version and self.entities == value.entities

    @property
    def version(self) -> int:
        return self._raw.header.version

    def entities_for_layer(self, layer: int) -> Iterator[Entity]:
        for entity in self.entities:
            if entity.layer_state(layer):
                yield entity

    @property
    def entities(self) -> list[Entity]:
        return self._raw.entities

    @entities.setter
    def entities(self, value: list[Entity]) -> None:
        self._raw.entities = value

    def get_entity(self, entity_id: int) -> Entity:
        entity_idx = 0
        for entity in self.entities:
            if entity.size == 0:
                continue
            if entity.entity_id == entity_id:
                break
            entity_idx += 1
        else:
            raise ValueError(f"No entity with ID {entity_id} found!")
        return entity

    def get_max_entity_id(self) -> int:
        entity_id = 0
        for entity in self.entities:
            if entity.entity_id > entity_id:
                entity_id = entity.entity_id
        return entity_id

    def append_entity(self, template: Entity) -> int:
        new_entity_id = self.get_max_entity_id() + 1
        template.header.entity_id = new_entity_id
        self.entities.append(Entity.create(template))
        return new_entity_id
