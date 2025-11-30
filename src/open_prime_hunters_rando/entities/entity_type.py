# mypy: disable-error-code="attr-defined"
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

from open_prime_hunters_rando.constants import EnumAdapter, Vec3, Vec4


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
    "data" / Padded(60, Switch(construct.this.type, volume_types)),  # type:ignore
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
    "fields" / Padded(400, Switch(construct.this.enemy_type, enemy_to_spawn_field)),  # type:ignore
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

RawEntityEntry = Struct(*raw_entry_fields)  # type:ignore

EntityEntry = Struct(
    *raw_entry_fields,  # type:ignore
    StopIf(this._data_offset == 0),
    "_entity_type" / Rebuild(Peek(Pointer(this._data_offset, EntityTypeConstruct)), this.data.header.entity_type),
    "data" / Pointer(this._data_offset, Aligned(4, Switch(this._entity_type, types_to_construct))),  # type:ignore
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


class Platform:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def no_port(self) -> int:
        return self._raw.data.no_port

    @no_port.setter
    def no_port(self, value: int) -> None:
        self._raw.data.no_port = value

    @property
    def model_id(self) -> int:
        return self._raw.data.model_id

    @model_id.setter
    def model_id(self, value: int) -> None:
        self._raw.data.model_id = value

    @property
    def parent_id(self) -> int:
        return self._raw.data.parent_id

    @parent_id.setter
    def parent_id(self, value: int) -> None:
        self._raw.data.parent_id = value

    @property
    def active(self) -> bool:
        return self._raw.data.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.data.active = value

    @property
    def delay(self) -> int:
        return self._raw.data.delay

    @delay.setter
    def delay(self, value: int) -> None:
        self._raw.data.delay = value

    @property
    def scan_data1(self) -> int:
        return self._raw.data.scan_data1

    @scan_data1.setter
    def scan_data1(self, value: int) -> None:
        self._raw.data.scan_data1 = value

    @property
    def scan_message_target(self) -> int:
        return self._raw.data.scan_message_target

    @scan_message_target.setter
    def scan_message_target(self, value: int) -> None:
        self._raw.data.scan_message_target = value

    @property
    def scan_message(self) -> Message:
        return self._raw.data.scan_message

    @scan_message.setter
    def scan_message(self, value: Message) -> None:
        self._raw.data.scan_message = value

    @property
    def scan_data2(self) -> int:
        return self._raw.data.scan_data2

    @scan_data2.setter
    def scan_data2(self, value: int) -> None:
        self._raw.data.scan_data2 = value

    @property
    def position_count(self) -> int:
        return self._raw.data.position_count

    @position_count.setter
    def position_count(self, value: int) -> None:
        self._raw.data.position_count = value

    @property
    def positions(self) -> list[Vec3]:
        return self._raw.data.positions

    @positions.setter
    def positions(self, value: list[Vec3]) -> None:
        self._raw.data.positions = value

    @property
    def rotations(self) -> list[Vec4]:
        return self._raw.data.rotations

    @rotations.setter
    def rotations(self, value: list[Vec4]) -> None:
        self._raw.data.rotations = value

    @property
    def position_offset(self) -> Vec3:
        return self._raw.data.position_offset

    @position_offset.setter
    def position_offset(self, value: Vec3) -> None:
        self._raw.data.position_offset = value

    @property
    def forward_speed(self) -> int:
        return self._raw.data.forward_speed

    @forward_speed.setter
    def forward_speed(self, value: float) -> None:
        self._raw.data.forward_speed = value

    @property
    def backward_speed(self) -> float:
        return self._raw.data.backward_speed

    @backward_speed.setter
    def backward_speed(self, value: float) -> None:
        self._raw.data.backward_speed = value

    @property
    def portal_name(self) -> str:
        return self._raw.data.portal_name

    @portal_name.setter
    def portal_name(self, value: str) -> None:
        self._raw.data.portal_name = value

    @property
    def movement_type(self) -> int:
        return self._raw.data.movement_type

    @movement_type.setter
    def movement_type(self, value: int) -> None:
        self._raw.data.movement_type = value

    @property
    def for_cutscene(self) -> int:
        return self._raw.data.for_cutscene

    @for_cutscene.setter
    def for_cutscene(self, value: int) -> None:
        self._raw.data.for_cutscene = value

    @property
    def reverse_type(self) -> int:
        return self._raw.data.reverse_type

    @reverse_type.setter
    def reverse_type(self, value: int) -> None:
        self._raw.data.reverse_type = value

    def flags(self, flag: PlatformFlags) -> bool:
        return self._raw.flags[flag.name]

    def set_flags(self, flag: PlatformFlags, state: bool) -> None:
        self._raw.effect_flags[flag.name] = state

    @property
    def contact_damage(self) -> int:
        return self._raw.data.contact_damage

    @contact_damage.setter
    def contact_damage(self, value: int) -> None:
        self._raw.data.contact_damage = value

    @property
    def beam_spawn_direction(self) -> Vec3:
        return self._raw.data.beam_spawn_direction

    @beam_spawn_direction.setter
    def beam_spawn_direction(self, value: Vec3) -> None:
        self._raw.data.beam_spawn_direction = value

    @property
    def beam_spawn_position(self) -> Vec3:
        return self._raw.data.beam_spawn_position

    @beam_spawn_position.setter
    def beam_spawn_position(self, value: Vec3) -> None:
        self._raw.data.beam_spawn_position = value

    @property
    def beam_id(self) -> int:
        return self._raw.data.beam_id

    @beam_id.setter
    def beam_id(self, value: int) -> None:
        self._raw.data.beam_id = value

    @property
    def beam_interval(self) -> int:
        return self._raw.data.beam_interval

    @beam_interval.setter
    def beam_interval(self, value: int) -> None:
        self._raw.data.beam_interval = value

    @property
    def beam_on_intervals(self) -> int:
        return self._raw.data.beam_on_intervals

    @beam_on_intervals.setter
    def beam_on_intervals(self, value: int) -> None:
        self._raw.data.beam_on_intervals = value

    @property
    def resist_effect_id(self) -> int:
        return self._raw.data.resist_effect_id

    @resist_effect_id.setter
    def resist_effect_id(self, value: int) -> None:
        self._raw.data.resist_effect_id = value

    @property
    def health(self) -> int:
        return self._raw.data.health

    @health.setter
    def health(self, value: int) -> None:
        self._raw.data.health = value

    @property
    def effectiveness(self) -> int:
        return self._raw.data.effectiveness

    @effectiveness.setter
    def effectiveness(self, value: int) -> None:
        self._raw.data.effectiveness = value

    @property
    def damage_effect_id(self) -> int:
        return self._raw.data.damage_effect_id

    @damage_effect_id.setter
    def damage_effect_id(self, value: int) -> None:
        self._raw.data.damage_effect_id = value

    @property
    def dead_effect_id(self) -> int:
        return self._raw.data.dead_effect_id

    @dead_effect_id.setter
    def dead_effect_id(self, value: int) -> None:
        self._raw.data.dead_effect_id = value

    @property
    def item_chance(self) -> int:
        return self._raw.data.item_chance

    @item_chance.setter
    def item_chance(self, value: int) -> None:
        self._raw.data.item_chance = value

    @property
    def item_type(self) -> ItemType:
        return self._raw.data.item_type

    @item_type.setter
    def item_type(self, value: ItemType) -> None:
        self._raw.data.item_type = value

    @property
    def beam_hit_message_target(self) -> int:
        return self._raw.data.beam_hit_message_target

    @beam_hit_message_target.setter
    def beam_hit_message_target(self, value: int) -> None:
        self._raw.data.beam_hit_message_target = value

    @property
    def beam_hit_message(self) -> Message:
        return self._raw.data.beam_hit_message

    @beam_hit_message.setter
    def beam_hit_message(self, value: Message) -> None:
        self._raw.data.beam_hit_message = value

    @property
    def beam_hit_message_param1(self) -> int:
        return self._raw.data.beam_hit_message_param1

    @beam_hit_message_param1.setter
    def beam_hit_message_param1(self, value: int) -> None:
        self._raw.data.beam_hit_message_param1 = value

    @property
    def beam_hit_message_param2(self) -> int:
        return self._raw.data.beam_hit_message_param2

    @beam_hit_message_param2.setter
    def beam_hit_message_param2(self, value: int) -> None:
        self._raw.data.beam_hit_message_param2 = value

    @property
    def player_collision_message_target(self) -> int:
        return self._raw.data.player_collision_message_target

    @player_collision_message_target.setter
    def player_collision_message_target(self, value: int) -> None:
        self._raw.data.player_collision_message_target = value

    @property
    def player_collision_message(self) -> Message:
        return self._raw.data.player_collision_message

    @player_collision_message.setter
    def player_collision_message(self, value: Message) -> None:
        self._raw.data.player_collision_message = value

    @property
    def player_collision_message_param1(self) -> int:
        return self._raw.data.player_collision_message_param1

    @player_collision_message_param1.setter
    def player_collision_message_param1(self, value: int) -> None:
        self._raw.data.player_collision_message_param1 = value

    @property
    def player_collision_message_param2(self) -> int:
        return self._raw.data.player_collision_message_param2

    @player_collision_message_param2.setter
    def player_collision_message_param2(self, value: int) -> None:
        self._raw.data.player_collision_message_param2 = value

    @property
    def dead_message_target(self) -> int:
        return self._raw.data.dead_message_target

    @dead_message_target.setter
    def dead_message_target(self, value: int) -> None:
        self._raw.data.dead_message_target = value

    @property
    def dead_message(self) -> Message:
        return self._raw.data.dead_message

    @dead_message.setter
    def dead_message(self, value: Message) -> None:
        self._raw.data.dead_message = value

    @property
    def dead_message_param1(self) -> int:
        return self._raw.data.dead_message_param1

    @dead_message_param1.setter
    def dead_message_param1(self, value: int) -> None:
        self._raw.data.dead_message_param1 = value

    @property
    def dead_message_param2(self) -> int:
        return self._raw.data.dead_message_param2

    @dead_message_param2.setter
    def dead_message_param2(self, value: int) -> None:
        self._raw.data.dead_message_param2 = value

    @property
    def lifetime_message1_index(self) -> int:
        return self._raw.data.lifetime_message1_target

    @property
    def lifetime_message1_target(self) -> int:
        return self._raw.data.lifetime_message1_target

    @lifetime_message1_target.setter
    def lifetime_message1_target(self, value: int) -> None:
        self._raw.data.lifetime_message1_target = value

    @property
    def lifetime_message1(self) -> Message:
        return self._raw.data.lifetime_message1

    @lifetime_message1.setter
    def lifetime_message1(self, value: Message) -> None:
        self._raw.data.lifetime_message1 = value

    @property
    def lifetime_message1_param1(self) -> int:
        return self._raw.data.lifetime_message1_param1

    @lifetime_message1_param1.setter
    def lifetime_message1_param1(self, value: int) -> None:
        self._raw.data.lifetime_message1_param1 = value

    @property
    def lifetime_message1_param2(self) -> int:
        return self._raw.data.lifetime_message1_param2

    @lifetime_message1_param2.setter
    def lifetime_message1_param2(self, value: int) -> None:
        self._raw.data.lifetime_message1_param2 = value

    @property
    def lifetime_message2_index(self) -> int:
        return self._raw.data.lifetime_message2_target

    @property
    def lifetime_message2_target(self) -> int:
        return self._raw.data.lifetime_message2_target

    @lifetime_message2_target.setter
    def lifetime_message2_target(self, value: int) -> None:
        self._raw.data.lifetime_message2_target = value

    @property
    def lifetime_message2(self) -> Message:
        return self._raw.data.lifetime_message2

    @lifetime_message2.setter
    def lifetime_message2(self, value: Message) -> None:
        self._raw.data.lifetime_message2 = value

    @property
    def lifetime_message2_param1(self) -> int:
        return self._raw.data.lifetime_message2_param1

    @lifetime_message2_param1.setter
    def lifetime_message2_param1(self, value: int) -> None:
        self._raw.data.lifetime_message2_param1 = value

    @property
    def lifetime_message2_param2(self) -> int:
        return self._raw.data.lifetime_message2_param2

    @lifetime_message2_param2.setter
    def lifetime_message2_param2(self, value: int) -> None:
        self._raw.data.lifetime_message2_param2 = value

    @property
    def lifetime_message3_index(self) -> int:
        return self._raw.data.lifetime_message3_target

    @property
    def lifetime_message3_target(self) -> int:
        return self._raw.data.lifetime_message3_target

    @lifetime_message3_target.setter
    def lifetime_message3_target(self, value: int) -> None:
        self._raw.data.lifetime_message3_target = value

    @property
    def lifetime_message3(self) -> Message:
        return self._raw.data.lifetime_message3

    @lifetime_message3.setter
    def lifetime_message3(self, value: Message) -> None:
        self._raw.data.lifetime_message3 = value

    @property
    def lifetime_message3_param1(self) -> int:
        return self._raw.data.lifetime_message3_param1

    @lifetime_message3_param1.setter
    def lifetime_message3_param1(self, value: int) -> None:
        self._raw.data.lifetime_message3_param1 = value

    @property
    def lifetime_message3_param2(self) -> int:
        return self._raw.data.lifetime_message3_param2

    @lifetime_message3_param2.setter
    def lifetime_message3_param2(self, value: int) -> None:
        self._raw.data.lifetime_message3_param2 = value

    @property
    def lifetime_message4_index(self) -> int:
        return self._raw.data.lifetime_message4_target

    @property
    def lifetime_message4_target(self) -> int:
        return self._raw.data.lifetime_message4_target

    @lifetime_message4_target.setter
    def lifetime_message4_target(self, value: int) -> None:
        self._raw.data.lifetime_message4_target = value

    @property
    def lifetime_message4(self) -> Message:
        return self._raw.data.lifetime_message4

    @lifetime_message4.setter
    def lifetime_message4(self, value: Message) -> None:
        self._raw.data.lifetime_message4 = value

    @property
    def lifetime_message4_param1(self) -> int:
        return self._raw.data.lifetime_message4_param1

    @lifetime_message4_param1.setter
    def lifetime_message4_param1(self, value: int) -> None:
        self._raw.data.lifetime_message4_param1 = value

    @property
    def lifetime_message4_param2(self) -> int:
        return self._raw.data.lifetime_message4_param2

    @lifetime_message4_param2.setter
    def lifetime_message4_param2(self, value: int) -> None:
        self._raw.data.lifetime_message4_param2 = value


class BoxVolumeType:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def box_vector1(self) -> Vec3:
        return self._raw.data.box_vector1

    @box_vector1.setter
    def box_vector1(self, value: Vec3) -> None:
        self._raw.data.box_vector1 = value

    @property
    def box_vector2(self) -> Vec3:
        return self._raw.data.box_vector2

    @box_vector2.setter
    def box_vector2(self, value: Vec3) -> None:
        self._raw.data.box_vector2 = value

    @property
    def box_vector3(self) -> Vec3:
        return self._raw.data.box_vector3

    @box_vector3.setter
    def box_vector3(self, value: Vec3) -> None:
        self._raw.data.box_vector3 = value

    @property
    def box_position(self) -> Vec3:
        return self._raw.data.box_position

    @box_position.setter
    def box_position(self, value: Vec3) -> None:
        self._raw.data.box_position = value

    @property
    def box_dot1(self) -> float:
        return self._raw.data.box_dot1

    @box_dot1.setter
    def box_dot1(self, value: float) -> None:
        self._raw.data.box_dot1 = value

    @property
    def box_dot2(self) -> float:
        return self._raw.data.box_dot2

    @box_dot2.setter
    def box_dot2(self, value: float) -> None:
        self._raw.data.box_dot2 = value

    @property
    def box_dot3(self) -> float:
        return self._raw.data.box_dot3

    @box_dot3.setter
    def box_dot3(self, value: float) -> None:
        self._raw.data.box_dot3 = value


class CylinderVolumeType:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def cylinder_vector(self) -> Vec3:
        return self._raw.data.cylinder_vector

    @cylinder_vector.setter
    def cylinder_vector(self, value: Vec3) -> None:
        self._raw.data.cylinder_vector = value

    @property
    def cylinder_position(self) -> Vec3:
        return self._raw.data.cylinder_position

    @cylinder_position.setter
    def cylinder_position(self, value: Vec3) -> None:
        self._raw.data.cylinder_position = value

    @property
    def cylinder_radius(self) -> float:
        return self._raw.data.cylinder_radius

    @cylinder_radius.setter
    def cylinder_radius(self, value: float) -> None:
        self._raw.data.cylinder_radius = value

    @property
    def cylinder_dot(self) -> float:
        return self._raw.data.cylinder_dot

    @cylinder_dot.setter
    def cylinder_dot(self, value: float) -> None:
        self._raw.data.cylinder_dot = value


class SphereVolumeType:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def sphere_position(self) -> Vec3:
        return self._raw.data.sphere_position

    @sphere_position.setter
    def sphere_position(self, value: Vec3) -> None:
        self._raw.data.sphere_position = value

    @property
    def sphere_radius(self) -> float:
        return self._raw.data.sphere_radius

    @sphere_radius.setter
    def sphere_radius(self, value: float) -> None:
        self._raw.data.sphere_radius = value


class VolumeProperties:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def type(self) -> VolumeType:
        return self._raw.volume.type

    @type.setter
    def type(self, value: VolumeType) -> None:
        self._raw.volume.type = value

    def set_box(self) -> BoxVolumeType:
        return BoxVolumeType(self._raw.volume.data)

    def set_cylinder(self) -> CylinderVolumeType:
        return CylinderVolumeType(self._raw.volume.data)

    def set_sphere(self) -> SphereVolumeType:
        return SphereVolumeType(self._raw.volume.data)


class Object:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def flags(self, flag: ObjectFlags) -> bool:
        return self._raw.flags[flag.name]

    def set_flags(self, flag: ObjectFlags, state: bool) -> None:
        self._raw.flags[flag.name] = state

    def effect_flags(self, effect_flag: ObjectEffectFlags) -> bool:
        return self._raw.effect_flags[effect_flag.name]

    def set_effect_flags(self, effect_flag: ObjectEffectFlags, state: bool) -> None:
        self._raw.effect_flags[effect_flag.name] = state

    @property
    def model_id(self) -> int:
        return self._raw.model_id

    @model_id.setter
    def model_id(self, value: int) -> None:
        self._raw.model_id = value

    @property
    def linked_entity(self) -> int:
        return self._raw.linked_entity

    @linked_entity.setter
    def linked_entity(self, value: int) -> None:
        self._raw.linked_entity = value

    @property
    def scan_id(self) -> int:
        return self._raw.scan_id

    @scan_id.setter
    def scan_id(self, value: int) -> None:
        self._raw.scan_id = value

    @property
    def scan_message_target(self) -> int:
        return self._raw.scan_message_target

    @scan_message_target.setter
    def scan_message_target(self, value: int) -> None:
        self._raw.scan_message_target = value

    @property
    def scan_message(self) -> Message:
        return self._raw.scan_message

    @scan_message.setter
    def scan_message(self, value: Message) -> None:
        self._raw.scan_message = value

    @property
    def effect_id(self) -> int:
        return self._raw.effect_id

    @effect_id.setter
    def effect_id(self, value: int) -> None:
        self._raw.effect_id = value

    @property
    def effect_interval(self) -> int:
        return self._raw.effect_interval

    @effect_interval.setter
    def effect_interval(self, value: int) -> None:
        self._raw.effect_interval = value

    @property
    def effect_on_inverals(self) -> int:
        return self._raw.effect_on_inverals

    @effect_on_inverals.setter
    def effect_on_inverals(self, value: int) -> None:
        self._raw.effect_on_inverals = value

    @property
    def effect_position_offset(self) -> Vec3:
        return self._raw.effect_position_offset

    @effect_position_offset.setter
    def effect_position_offset(self, value: Vec3) -> None:
        self._raw.effect_position_offset = value

    def get_volume(self) -> VolumeType:
        return VolumeType(self._raw.volume)


class PlayerSpawn:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def availability(self) -> int:
        return self._raw.availability

    @availability.setter
    def availability(self, value: int) -> None:
        self._raw.availability = value

    @property
    def active(self) -> int:
        return self._raw.active

    @active.setter
    def active(self, value: int) -> None:
        self._raw.active = value

    @property
    def team_index(self) -> int:
        return self._raw.team_index

    @team_index.setter
    def team_index(self, value: int) -> None:
        self._raw.team_index = value


class Door:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def node_name(self) -> str:
        return self._raw.node_name

    @node_name.setter
    def node_name(self, value: str) -> None:
        self._raw.node_name = value

    @property
    def palette_id(self) -> PaletteId:
        return self._raw.palette_id

    @palette_id.setter
    def palette_id(self, value: PaletteId) -> None:
        self._raw.palette_id = value

    @property
    def door_type(self) -> DoorType:
        return self._raw.palette_id

    @door_type.setter
    def door_type(self, value: DoorType) -> None:
        self._raw.door_type = value

    @property
    def connector_id(self) -> int:
        return self._raw.connector_id

    @connector_id.setter
    def connector_id(self, value: int) -> None:
        self._raw.connector_id = value

    @property
    def target_layer_id(self) -> int:
        return self._raw.target_layer_id

    @target_layer_id.setter
    def target_layer_id(self, value: int) -> None:
        self._raw.target_layer_id = value

    @property
    def locked(self) -> bool:
        return self._raw.locked

    @locked.setter
    def locked(self, value: bool) -> None:
        self._raw.locked = value

    @property
    def out_connector_id(self) -> int:
        return self._raw.out_connector_id

    @out_connector_id.setter
    def out_connector_id(self, value: int) -> None:
        self._raw.out_connector_id = value

    @property
    def out_loader_id(self) -> int:
        return self._raw.out_loader_id

    @out_loader_id.setter
    def out_loader_id(self, value: int) -> None:
        self._raw.out_loader_id = value

    @property
    def entity_file_name(self) -> str:
        return self._raw.entity_file_name

    @entity_file_name.setter
    def entity_file_name(self, value: str) -> None:
        self._raw.entity_file_name = value

    @property
    def room_name(self) -> str:
        return self._raw.room_name

    @room_name.setter
    def room_name(self, value: str) -> None:
        self._raw.room_name = value


class ItemSpawn:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def parent_id(self) -> int:
        return self._raw.parent_id

    @parent_id.setter
    def parent_id(self, value: int) -> None:
        self._raw.parent_id = value

    @property
    def item_type(self) -> ItemType:
        return self._raw.item_type

    @item_type.setter
    def item_type(self, value: ItemType) -> None:
        self._raw.item_type = value

    @property
    def enabled(self) -> bool:
        return self._raw.enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._raw.enabled = value

    @property
    def has_base(self) -> bool:
        return self._raw.has_base

    @has_base.setter
    def has_base(self, value: bool) -> None:
        self._raw.has_base = value

    @property
    def always_active(self) -> bool:
        return self._raw.always_active

    @always_active.setter
    def always_active(self, value: bool) -> None:
        self._raw.always_active = value

    @property
    def max_spawn_count(self) -> int:
        return self._raw.max_spawn_count

    @max_spawn_count.setter
    def max_spawn_count(self, value: int) -> None:
        self._raw.max_spawn_count = value

    @property
    def spawn_interval(self) -> int:
        return self._raw.spawn_interval

    @spawn_interval.setter
    def spawn_interval(self, value: int) -> None:
        self._raw.spawn_interval = value

    @property
    def spawn_delay(self) -> int:
        return self._raw.spawn_delay

    @spawn_delay.setter
    def spawn_delay(self, value: int) -> None:
        self._raw.spawn_delay = value

    @property
    def notify_entity_id(self) -> int:
        return self._raw.notify_entity_id

    @notify_entity_id.setter
    def notify_entity_id(self, value: int) -> None:
        self._raw.notify_entity_id = value

    @property
    def collected_message(self) -> Message:
        return self._raw.collected_message

    @collected_message.setter
    def collected_message(self, value: Message) -> None:
        self._raw.collected_message = value

    @property
    def collected_message_param1(self) -> int:
        return self._raw.collected_message_param1

    @collected_message_param1.setter
    def collected_message_param1(self, value: int) -> None:
        self._raw.collected_message_param1 = value

    @property
    def collected_message_param2(self) -> int:
        return self._raw.collected_message_param2

    @collected_message_param2.setter
    def collected_message_param2(self, value: int) -> None:
        self._raw.collected_message_param2 = value


class WarWaspField:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.volume0)

    def get_volume1(self) -> VolumeType:
        return VolumeType(self._raw.volume1)

    def get_volume2(self) -> VolumeType:
        return VolumeType(self._raw.volume2)

    @property
    def movement_vectors(self) -> list[Vec3]:
        return self._raw.movement_vectors

    @movement_vectors.setter
    def movement_vectors(self, value: list[Vec3]) -> None:
        self._raw.movement_vectors = value

    @property
    def position_count(self) -> int:
        return self._raw.position_count

    @position_count.setter
    def position_count(self, value: int) -> None:
        self._raw.position_count = value

    @property
    def movement_type(self) -> int:
        return self._raw.movement_type

    @movement_type.setter
    def movement_type(self, value: int) -> None:
        self._raw.movement_type = value


class Field0:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.volume0)

    def get_volume1(self) -> VolumeType:
        return VolumeType(self._raw.volume1)

    def get_volume2(self) -> VolumeType:
        return VolumeType(self._raw.volume2)

    def get_volume3(self) -> VolumeType:
        return VolumeType(self._raw.volume3)


class Field1:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def war_wasp(self) -> WarWaspField:
        return self._raw.war_wasp

    def get_war_wasp(self) -> WarWaspField:
        return WarWaspField(self._raw.war_wasp)


class Field2:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.volume0)

    @property
    def path_vector(self) -> Vec3:
        return self._raw.path_vector

    @path_vector.setter
    def path_vector(self, value: Vec3) -> None:
        self._raw.path_vector = value

    def get_volume1(self) -> VolumeType:
        return VolumeType(self._raw.volume1)

    def get_volume2(self) -> VolumeType:
        return VolumeType(self._raw.volume2)


class Field3:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.volume0)

    @property
    def facing(self) -> Vec3:
        return self._raw.facing

    @facing.setter
    def facing(self, value: Vec3) -> None:
        self._raw.facing = value

    @property
    def position(self) -> Vec3:
        return self._raw.position

    @position.setter
    def position(self, value: Vec3) -> None:
        self._raw.position = value

    @property
    def idle_range(self) -> Vec3:
        return self._raw.idle_range

    @idle_range.setter
    def idle_range(self, value: Vec3) -> None:
        self._raw.idle_range = value


class Field4:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.volume0)

    @property
    def position(self) -> Vec3:
        return self._raw.position

    @position.setter
    def position(self, value: Vec3) -> None:
        self._raw.position = value

    @property
    def weave_offset(self) -> int:
        return self._raw.weave_offset

    @weave_offset.setter
    def weave_offset(self, value: int) -> None:
        self._raw.weave_offset = value

    @property
    def field(self) -> int:
        return self._raw.field

    @field.setter
    def field(self, value: int) -> None:
        self._raw.field = value


class Field5:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def enemy_subtype(self) -> int:
        return self._raw.enemy_subtype

    @enemy_subtype.setter
    def enemy_subtype(self, value: int) -> None:
        self._raw.enemy_subtype = value

    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.volume0)

    def get_volume1(self) -> VolumeType:
        return VolumeType(self._raw.volume1)

    def get_volume2(self) -> VolumeType:
        return VolumeType(self._raw.volume2)

    def get_volume3(self) -> VolumeType:
        return VolumeType(self._raw.volume3)


class Field6:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def enemy_subtype(self) -> int:
        return self._raw.enemy_subtype

    @enemy_subtype.setter
    def enemy_subtype(self, value: int) -> None:
        self._raw.enemy_subtype = value

    @property
    def enemy_version(self) -> int:
        return self._raw.enemy_version

    @enemy_version.setter
    def enemy_version(self, value: int) -> None:
        self._raw.enemy_version = value

    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.volume0)

    def get_volume1(self) -> VolumeType:
        return VolumeType(self._raw.volume1)

    def get_volume2(self) -> VolumeType:
        return VolumeType(self._raw.volume2)

    def get_volume3(self) -> VolumeType:
        return VolumeType(self._raw.volume3)


class Field7:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def enemy_health(self) -> int:
        return self._raw.enemy_health

    @enemy_health.setter
    def enemy_health(self, value: int) -> None:
        self._raw.enemy_health = value

    @property
    def enemy_damage(self) -> int:
        return self._raw.enemy_damage

    @enemy_damage.setter
    def enemy_damage(self, value: int) -> None:
        self._raw.enemy_damage = value

    @property
    def enemy_subtype(self) -> int:
        return self._raw.enemy_subtype

    @enemy_subtype.setter
    def enemy_subtype(self, value: int) -> None:
        self._raw.enemy_subtype = value

    def war_wasp(self) -> WarWaspField:
        return self._raw.war_wasp

    def get_war_wasp(self) -> WarWaspField:
        return WarWaspField(self._raw.war_wasp)


class Field8:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def enemy_subtype(self) -> int:
        return self._raw.enemy_subtype

    @enemy_subtype.setter
    def enemy_subtype(self, value: int) -> None:
        self._raw.enemy_subtype = value

    @property
    def enemy_version(self) -> int:
        return self._raw.enemy_version

    @enemy_version.setter
    def enemy_version(self, value: int) -> None:
        self._raw.enemy_version = value

    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.volume0)


class Field9:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def hunter_id(self) -> Hunter:
        return self._raw.hunter_id

    @hunter_id.setter
    def hunter_id(self, value: Hunter) -> None:
        self._raw.hunter_id = value

    @property
    def encounter_type(self) -> int:
        return self._raw.encounter_type

    @encounter_type.setter
    def encounter_type(self, value: int) -> None:
        self._raw.encounter_type = value

    @property
    def hunter_weapon(self) -> int:
        return self._raw.hunter_weapon

    @hunter_weapon.setter
    def hunter_weapon(self, value: int) -> None:
        self._raw.hunter_weapon = value

    @property
    def hunter_health(self) -> int:
        return self._raw.hunter_health

    @hunter_health.setter
    def hunter_health(self, value: int) -> None:
        self._raw.hunter_health = value

    @property
    def hunter_health_max(self) -> int:
        return self._raw.hunter_health_max

    @hunter_health_max.setter
    def hunter_health_max(self, value: int) -> None:
        self._raw.hunter_health_max = value

    @property
    def field(self) -> int:
        return self._raw.field

    @field.setter
    def field(self, value: int) -> None:
        self._raw.field = value

    @property
    def hunter_color(self) -> int:
        return self._raw.hunter_color

    @hunter_color.setter
    def hunter_color(self, value: int) -> None:
        self._raw.hunter_color = value

    @property
    def hunter_chance(self) -> int:
        return self._raw.hunter_chance

    @hunter_chance.setter
    def hunter_chance(self, value: int) -> None:
        self._raw.hunter_chance = value


class Field10:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def enemy_subtype(self) -> int:
        return self._raw.enemy_subtype

    @enemy_subtype.setter
    def enemy_subtype(self, value: int) -> None:
        self._raw.enemy_subtype = value

    @property
    def enemy_version(self) -> int:
        return self._raw.enemy_version

    @enemy_version.setter
    def enemy_version(self, value: int) -> None:
        self._raw.enemy_version = value

    def get_volume0(self) -> VolumeType:
        return VolumeType(self._raw.volume0)

    def get_volume1(self) -> VolumeType:
        return VolumeType(self._raw.volume1)

    @property
    def index(self) -> int:
        return self._raw.index

    @index.setter
    def index(self, value: int) -> None:
        self._raw.index = value


class Field11:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def sphere1_position(self) -> Vec3:
        return self._raw.sphere1_position

    @sphere1_position.setter
    def sphere1_position(self, value: Vec3) -> None:
        self._raw.sphere1_position = value

    @property
    def sphere1_radius(self) -> float:
        return self._raw.sphere1_radius

    @sphere1_radius.setter
    def sphere1_radius(self, value: float) -> None:
        self._raw.sphere1_radius = value

    @property
    def sphere2_position(self) -> Vec3:
        return self._raw.sphere2_position

    @sphere2_position.setter
    def sphere2_position(self, value: Vec3) -> None:
        self._raw.sphere2_position = value

    @property
    def sphere2_radius(self) -> float:
        return self._raw.sphere2_radiusfield3

    @sphere2_radius.setter
    def sphere2_radius(self, value: float) -> None:
        self._raw.sphere2_radius = value


class Field12:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def field1(self) -> Vec3:
        return self._raw.field1

    @field1.setter
    def field1(self, value: Vec3) -> None:
        self._raw.field1 = value

    @property
    def field2(self) -> int:
        return self._raw.field2

    @field2.setter
    def field2(self, value: int) -> None:
        self._raw.field2 = value

    @property
    def field3(self) -> int:
        return self._raw.field3

    @field3.setter
    def field3(self, value: int) -> None:
        self._raw.field3 = value


class EnemySpawn:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def enemy_type(self) -> EnemyType:
        return self._raw.enemy_type

    @enemy_type.setter
    def enemy_type(self, value: EnemyType) -> None:
        self._raw.enemy_type = value

    def fields(self) -> Container:
        return self._raw.fields

    def get_enemy_spawn_field_0(self) -> Field0:
        return Field0(self._raw.fields)

    def get_enemy_spawn_field_1(self) -> Field1:
        return Field1(self._raw.fields)

    def get_enemy_spawn_field_2(self) -> Field2:
        return Field2(self._raw.fields)

    def get_enemy_spawn_field_3(self) -> Field3:
        return Field3(self._raw.fields)

    def get_enemy_spawn_field_4(self) -> Field4:
        return Field4(self._raw.fields)

    def get_enemy_spawn_field_5(self) -> Field5:
        return Field5(self._raw.fields)

    def get_enemy_spawn_field_6(self) -> Field6:
        return Field6(self._raw.fields)

    def get_enemy_spawn_field_7(self) -> Field7:
        return Field7(self._raw.fields)

    def get_enemy_spawn_field_8(self) -> Field8:
        return Field8(self._raw.fields)

    def get_enemy_spawn_field_9(self) -> Field9:
        return Field9(self._raw.fields)

    def get_enemy_spawn_field_10(self) -> Field10:
        return Field10(self._raw.fields)

    def get_enemy_spawn_field_11(self) -> Field11:
        return Field11(self._raw.fields)

    def get_enemy_spawn_field_12(self) -> Field12:
        return Field12(self._raw.fields)

    @property
    def linked_entity_id(self) -> int:
        return self._raw.linked_entity_id

    @linked_entity_id.setter
    def linked_entity_id(self, value: int) -> None:
        self._raw.linked_entity_id = value

    @property
    def spawn_limit(self) -> int:
        return self._raw.spawn_limit

    @spawn_limit.setter
    def spawn_limit(self, value: int) -> None:
        self._raw.spawn_limit = value

    @property
    def spawn_total(self) -> int:
        return self._raw.spawn_total

    @spawn_total.setter
    def spawn_total(self, value: int) -> None:
        self._raw.spawn_total = value

    @property
    def spawn_count(self) -> int:
        return self._raw.spawn_count

    @spawn_count.setter
    def spawn_count(self, value: int) -> None:
        self._raw.spawn_count = value

    @property
    def active(self) -> bool:
        return self._raw.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.active = value

    @property
    def always_active(self) -> bool:
        return self._raw.always_active

    @always_active.setter
    def always_active(self, value: bool) -> None:
        self._raw.always_active = value

    @property
    def item_chance(self) -> int:
        return self._raw.item_chance

    @item_chance.setter
    def item_chance(self, value: int) -> None:
        self._raw.item_chance = value

    @property
    def spawner_health(self) -> int:
        return self._raw.spawner_health

    @spawner_health.setter
    def spawner_health(self, value: int) -> None:
        self._raw.spawner_health = value

    @property
    def cooldown_time(self) -> int:
        return self._raw.cooldown_time

    @cooldown_time.setter
    def cooldown_time(self, value: int) -> None:
        self._raw.cooldown_time = value

    @property
    def initial_cooldown(self) -> int:
        return self._raw.initial_cooldown

    @initial_cooldown.setter
    def initial_cooldown(self, value: int) -> None:
        self._raw.initial_cooldown = value

    @property
    def active_distance(self) -> float:
        return self._raw.active_distance

    @active_distance.setter
    def active_distance(self, value: float) -> None:
        self._raw.active_distance = value

    @property
    def enemy_active_distance(self) -> float:
        return self._raw.enemy_active_distance

    @enemy_active_distance.setter
    def enemy_active_distance(self, value: float) -> None:
        self._raw.enemy_active_distance = value

    @property
    def node_name(self) -> str:
        return self._raw.node_name

    @node_name.setter
    def node_name(self, value: str) -> None:
        self._raw.node_name = value

    @property
    def entity_id1(self) -> int:
        return self._raw.entity_id1

    @entity_id1.setter
    def entity_id1(self, value: int) -> None:
        self._raw.entity_id1 = value

    @property
    def message1(self) -> Message:
        return self._raw.message1

    @message1.setter
    def message1(self, value: Message) -> None:
        self._raw.message1 = value

    @property
    def entity_id2(self) -> int:
        return self._raw.entity_id2

    @entity_id2.setter
    def entity_id2(self, value: int) -> None:
        self._raw.entity_id2 = value

    @property
    def message2(self) -> Message:
        return self._raw.message2

    @message2.setter
    def message2(self, value: Message) -> None:
        self._raw.message2 = value

    @property
    def entity_id3(self) -> int:
        return self._raw.entity_id3

    @entity_id3.setter
    def entity_id3(self, value: int) -> None:
        self._raw.entity_id3 = value

    @property
    def message3(self) -> Message:
        return self._raw.message3

    @message3.setter
    def message3(self, value: Message) -> None:
        self._raw.message3 = value

    @property
    def item_type(self) -> ItemType:
        return self._raw.item_type

    @item_type.setter
    def item_type(self, value: ItemType) -> None:
        self._raw.item_type = value


class TriggerVolume:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def subtype(self) -> TriggerVolumeType:
        return self._raw.subtype

    @subtype.setter
    def subtype(self, value: TriggerVolumeType) -> None:
        self._raw.subtype = value

    def get_volume(self) -> VolumeType:
        return VolumeType(self._raw.volume)

    @property
    def active(self) -> bool:
        return self._raw.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.active = value

    @property
    def always_active(self) -> bool:
        return self._raw.always_active

    @always_active.setter
    def always_active(self, value: bool) -> None:
        self._raw.always_active = value

    @property
    def deactivate_after_use(self) -> bool:
        return self._raw.deactivate_after_use

    @deactivate_after_use.setter
    def deactivate_after_use(self, value: bool) -> None:
        self._raw.deactivate_after_use = value

    @property
    def repeat_delay(self) -> int:
        return self._raw.repeat_delay

    @repeat_delay.setter
    def repeat_delay(self, value: int) -> None:
        self._raw.repeat_delay = value

    @property
    def check_delay(self) -> int:
        return self._raw.check_delay

    @check_delay.setter
    def check_delay(self, value: int) -> None:
        self._raw.check_delay = value

    @property
    def required_state_bit(self) -> int:
        return self._raw.required_state_bit

    @required_state_bit.setter
    def required_state_bit(self, value: int) -> None:
        self._raw.required_state_bit = value

    def trigger_flags(self, flag: TriggerVolumeFlags) -> bool:
        return self._raw.trigger_flags[flag.name]

    def set_trigger_flags(self, flag: TriggerVolumeFlags, state: bool) -> None:
        self._raw.trigger_flags[flag.name] = state

    @property
    def trigger_threshold(self) -> int:
        return self._raw.trigger_threshold

    @trigger_threshold.setter
    def trigger_threshold(self, value: int) -> None:
        self._raw.trigger_threshold = value

    @property
    def parent_id(self) -> int:
        return self._raw.parent_id

    @parent_id.setter
    def parent_id(self, value: int) -> None:
        self._raw.parent_id = value

    @property
    def parent_message(self) -> Message:
        return self._raw.parent_message

    @parent_message.setter
    def parent_message(self, value: Message) -> None:
        self._raw.parent_message = value

    @property
    def parent_message_param1(self) -> int:
        return self._raw.parent_message_param1

    @parent_message_param1.setter
    def parent_message_param1(self, value: int) -> None:
        self._raw.parent_message_param1 = value

    @property
    def parent_message_param2(self) -> int:
        return self._raw.parent_message_param2

    @parent_message_param2.setter
    def parent_message_param2(self, value: int) -> None:
        self._raw.parent_message_param2 = value

    @property
    def child_id(self) -> int:
        return self._raw.child_id

    @child_id.setter
    def child_id(self, value: int) -> None:
        self._raw.child_id = value

    @property
    def child_message(self) -> Message:
        return self._raw.child_message

    @child_message.setter
    def child_message(self, value: Message) -> None:
        self._raw.child_message = value

    @property
    def child_message_param1(self) -> int:
        return self._raw.child_message_param1

    @child_message_param1.setter
    def child_message_param1(self, value: int) -> None:
        self._raw.child_message_param1 = value

    @property
    def child_message_param2(self) -> int:
        return self._raw.child_message_param2

    @child_message_param2.setter
    def child_message_param2(self, value: int) -> None:
        self._raw.child_message_param2 = value


class AreaVolume:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def get_volume(self) -> VolumeType:
        return VolumeType(self._raw.volume)

    @property
    def active(self) -> bool:
        return self._raw.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.active = value

    @property
    def always_active(self) -> bool:
        return self._raw.always_active

    @always_active.setter
    def always_active(self, value: bool) -> None:
        self._raw.always_active = value

    @property
    def allow_mulitple(self) -> bool:
        return self._raw.allow_mulitple

    @allow_mulitple.setter
    def allow_mulitple(self, value: bool) -> None:
        self._raw.allow_mulitple = value

    @property
    def message_delay(self) -> int:
        return self._raw.message_delay

    @message_delay.setter
    def message_delay(self, value: int) -> None:
        self._raw.message_delay = value

    @property
    def inside_message(self) -> Message:
        return self._raw.inside_message

    @inside_message.setter
    def inside_message(self, value: Message) -> None:
        self._raw.inside_message = value

    @property
    def inside_message_param1(self) -> int:
        return self._raw.inside_message_param1

    @inside_message_param1.setter
    def inside_message_param1(self, value: int) -> None:
        self._raw.inside_message_param1 = value

    @property
    def inside_message_param2(self) -> int:
        return self._raw.inside_message_param2

    @inside_message_param2.setter
    def inside_message_param2(self, value: int) -> None:
        self._raw.inside_message_param2 = value

    @property
    def parent_id(self) -> int:
        return self._raw.parent_id

    @parent_id.setter
    def parent_id(self, value: int) -> None:
        self._raw.parent_id = value

    @property
    def exit_message(self) -> Message:
        return self._raw.exit_message

    @exit_message.setter
    def exit_message(self, value: Message) -> None:
        self._raw.exit_message = value

    @property
    def exit_message_param1(self) -> int:
        return self._raw.exit_message_param1

    @exit_message_param1.setter
    def exit_message_param1(self, value: int) -> None:
        self._raw.exit_message_param1 = value

    @property
    def exit_message_param2(self) -> int:
        return self._raw.exit_message_param2

    @exit_message_param2.setter
    def exit_message_param2(self, value: int) -> None:
        self._raw.exit_message_param2 = value

    @property
    def child_id(self) -> int:
        return self._raw.child_id

    @child_id.setter
    def child_id(self, value: int) -> None:
        self._raw.child_id = value

    @property
    def cooldown(self) -> int:
        return self._raw.cooldown

    @cooldown.setter
    def cooldown(self, value: int) -> None:
        self._raw.cooldown = value

    @property
    def priority(self) -> int:
        return self._raw.priority

    @priority.setter
    def priority(self, value: int) -> None:
        self._raw.priority = value

    def trigger_flags(self, flag: TriggerVolumeFlags) -> bool:
        return self._raw.trigger_flags[flag.name]

    def set_trigger_flags(self, flag: TriggerVolumeFlags, state: bool) -> None:
        self._raw.trigger_flags[flag.name] = state


class JumpPad:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def parent_id(self) -> int:
        return self._raw.parent_id

    @parent_id.setter
    def parent_id(self, value: int) -> None:
        self._raw.parent_id = value

    def get_volume(self) -> VolumeType:
        return VolumeType(self._raw.volume)

    @property
    def beam_vector(self) -> Vec3:
        return self._raw.beam_vector

    @beam_vector.setter
    def beam_vector(self, value: Vec3) -> None:
        self._raw.beam_vector = value

    @property
    def speed(self) -> float:
        return self._raw.speed

    @speed.setter
    def speed(self, value: float) -> None:
        self._raw.speed = value

    @property
    def control_lock_time(self) -> int:
        return self._raw.control_lock_time

    @control_lock_time.setter
    def control_lock_time(self, value: int) -> None:
        self._raw.control_lock_time = value

    @property
    def cooldown_time(self) -> int:
        return self._raw.cooldown_time

    @cooldown_time.setter
    def cooldown_time(self, value: int) -> None:
        self._raw.cooldown_time = value

    @property
    def active(self) -> bool:
        return self._raw.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.active = value

    @property
    def model_id(self) -> int:
        return self._raw.model_id

    @model_id.setter
    def model_id(self, value: int) -> None:
        self._raw.model_id = value

    @property
    def beam_type(self) -> int:
        return self._raw.beam_type

    @beam_type.setter
    def beam_type(self, value: int) -> None:
        self._raw.beam_type = value

    def trigger_flags(self, flag: TriggerVolumeFlags) -> bool:
        return self._raw.trigger_flags[flag.name]

    def set_trigger_flags(self, flag: TriggerVolumeFlags, state: bool) -> None:
        self._raw.trigger_flags[flag.name] = state


class PointModule:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def next_id(self) -> int:
        return self._raw.next_id

    @next_id.setter
    def next_id(self, value: int) -> None:
        self._raw.next_id = value

    @property
    def prev_id(self) -> int:
        return self._raw.prev_id

    @prev_id.setter
    def prev_id(self, value: int) -> None:
        self._raw.prev_id = value

    @property
    def active(self) -> bool:
        return self._raw.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.active = value


class MorphCamera:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def get_volume(self) -> VolumeType:
        return VolumeType(self._raw.volume)


class OctolithFlag:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def team_id(self) -> int:
        return self._raw.team_id

    @team_id.setter
    def team_id(self, value: int) -> None:
        self._raw.team_id = value


class FlagBase:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def team_id(self) -> int:
        return self._raw.team_id

    @team_id.setter
    def team_id(self, value: int) -> None:
        self._raw.team_id = value

    def get_volume(self) -> VolumeType:
        return VolumeType(self._raw.volume)


class Teleporter:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def load_index(self) -> int:
        return self._raw.load_index

    @load_index.setter
    def load_index(self, value: int) -> None:
        self._raw.load_index = value

    @property
    def target_index(self) -> int:
        return self._raw.target_index

    @target_index.setter
    def target_index(self, value: int) -> None:
        self._raw.target_index = value

    @property
    def artifact_id(self) -> int:
        return self._raw.artifact_id

    @artifact_id.setter
    def artifact_id(self, value: int) -> None:
        self._raw.artifact_id = value

    @property
    def active(self) -> bool:
        return self._raw.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.active = value

    @property
    def invisible(self) -> bool:
        return self._raw.invisible

    @invisible.setter
    def invisible(self, value: bool) -> None:
        self._raw.invisible = value

    @property
    def entity_filename(self) -> str:
        return self._raw.entity_filename

    @entity_filename.setter
    def entity_filename(self, value: str) -> None:
        self._raw.entity_filename = value

    @property
    def target_position(self) -> Vec3:
        return self._raw.target_position

    @target_position.setter
    def target_position(self, value: Vec3) -> None:
        self._raw.target_position = value

    @property
    def node_name(self) -> str:
        return self._raw.node_name

    @node_name.setter
    def node_name(self, value: str) -> None:
        self._raw.node_name = value


class DefenseNode:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def get_volume(self) -> VolumeType:
        return VolumeType(self._raw.volume)


class LightSource:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def get_volume(self) -> VolumeType:
        return VolumeType(self._raw.volume)

    @property
    def light1_enabled(self) -> bool:
        return self._raw.light1_enabled

    @light1_enabled.setter
    def light1_enabled(self, value: bool) -> None:
        self._raw.light1_enabled = value

    @property
    def light1_color(self) -> Vec3:
        return self._raw.light1_color

    @light1_color.setter
    def light1_color(self, value: Vec3) -> None:
        self._raw.light1_color = value

    @property
    def light1_vector(self) -> Vec3:
        return self._raw.light1_vector

    @light1_vector.setter
    def light1_vector(self, value: Vec3) -> None:
        self._raw.light1_vector = value

    @property
    def light2_enabled(self) -> bool:
        return self._raw.light2_enabled

    @light2_enabled.setter
    def light2_enabled(self, value: bool) -> None:
        self._raw.light2_enabled = value

    @property
    def light2_color(self) -> Vec3:
        return self._raw.light2_color

    @light2_color.setter
    def light2_color(self, value: Vec3) -> None:
        self._raw.light2_color = value

    @property
    def light2_vector(self) -> Vec3:
        return self._raw.light2_vector

    @light2_vector.setter
    def light2_vector(self, value: Vec3) -> None:
        self._raw.light2_vector = value


class Artifact:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def model_id(self) -> int:
        return self._raw.model_id

    @model_id.setter
    def model_id(self, value: int) -> None:
        self._raw.model_id = value

    @property
    def artifact_id(self) -> int:
        return self._raw.artifact_id

    @artifact_id.setter
    def artifact_id(self, value: int) -> None:
        self._raw.artifact_id = value

    @property
    def active(self) -> bool:
        return self._raw.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.active = value

    @property
    def has_base(self) -> bool:
        return self._raw.has_base

    @has_base.setter
    def has_base(self, value: bool) -> None:
        self._raw.has_base = value

    @property
    def message1_target(self) -> int:
        return self._raw.message1_target

    @message1_target.setter
    def message1_target(self, value: int) -> None:
        self._raw.message1_target = value

    @property
    def message1(self) -> Message:
        return self._raw.message1

    @message1.setter
    def message1(self, value: Message) -> None:
        self._raw.message1 = value

    @property
    def message2_target(self) -> int:
        return self._raw.message2_target

    @message2_target.setter
    def message2_target(self, value: int) -> None:
        self._raw.message2_target = value

    @property
    def message2(self) -> Message:
        return self._raw.message2

    @message2.setter
    def message2(self, value: Message) -> None:
        self._raw.message2 = value

    @property
    def message3_target(self) -> int:
        return self._raw.message3_target

    @message3_target.setter
    def message3_target(self, value: int) -> None:
        self._raw.message3_target = value

    @property
    def message3(self) -> Message:
        return self._raw.message3

    @message3.setter
    def message3(self, value: Message) -> None:
        self._raw.message3 = value

    @property
    def linked_entity_id(self) -> int:
        return self._raw.linked_entity_id

    @linked_entity_id.setter
    def linked_entity_id(self, value: int) -> None:
        self._raw.linked_entity_id = value


class CameraSequence:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def sequence_id(self) -> int:
        return self._raw.sequence_id

    @sequence_id.setter
    def sequence_id(self, value: int) -> None:
        self._raw.sequence_id = value

    @property
    def handoff(self) -> bool:
        return self._raw.handoff

    @handoff.setter
    def handoff(self, value: bool) -> None:
        self._raw.handoff = value

    @property
    def loop(self) -> bool:
        return self._raw.loop

    @loop.setter
    def loop(self, value: bool) -> None:
        self._raw.loop = value

    @property
    def block_input(self) -> bool:
        return self._raw.block_input

    @block_input.setter
    def block_input(self, value: bool) -> None:
        self._raw.block_input = value

    @property
    def force_alt_form(self) -> bool:
        return self._raw.force_alt_form

    @force_alt_form.setter
    def force_alt_form(self, value: bool) -> None:
        self._raw.force_alt_form = value

    @property
    def force_biped_form(self) -> bool:
        return self._raw.force_biped_form

    @force_biped_form.setter
    def force_biped_form(self, value: bool) -> None:
        self._raw.force_biped_form = value

    @property
    def delay_frames(self) -> int:
        return self._raw.delay_frames

    @delay_frames.setter
    def delay_frames(self, value: int) -> None:
        self._raw.delay_frames = value

    @property
    def player_id1(self) -> int:
        return self._raw.player_id1

    @player_id1.setter
    def player_id1(self, value: int) -> None:
        self._raw.player_id1 = value

    @property
    def player_id2(self) -> int:
        return self._raw.player_id2

    @player_id2.setter
    def player_id2(self, value: int) -> None:
        self._raw.player_id2 = value

    @property
    def entity1(self) -> int:
        return self._raw.entity1

    @entity1.setter
    def entity1(self, value: int) -> None:
        self._raw.entity1 = value

    @property
    def entity2(self) -> int:
        return self._raw.entity2

    @entity2.setter
    def entity2(self, value: int) -> None:
        self._raw.entity2 = value

    @property
    def end_message_target_id(self) -> int:
        return self._raw.end_message_target_id

    @end_message_target_id.setter
    def end_message_target_id(self, value: int) -> None:
        self._raw.end_message_target_id = value

    @property
    def end_message(self) -> Message:
        return self._raw.end_message

    @end_message.setter
    def end_message(self, value: Message) -> None:
        self._raw.end_message = value

    @property
    def end_message_param(self) -> int:
        return self._raw.end_message_param

    @end_message_param.setter
    def end_message_param(self, value: int) -> None:
        self._raw.end_message_param = value


class ForceField:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def type(self) -> PaletteId:
        return self._raw.type

    @type.setter
    def type(self, value: PaletteId) -> None:
        self._raw.type = value

    @property
    def width(self) -> float:
        return self._raw.width

    @width.setter
    def width(self, value: float) -> None:
        self._raw.width = value

    @property
    def height(self) -> float:
        return self._raw.height

    @height.setter
    def height(self, value: float) -> None:
        self._raw.height = value

    @property
    def active(self) -> bool:
        return self._raw.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.active = value


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
        return self.header.entity_type

    @entity_type.setter
    def entity_type(self, value: EntityType) -> None:
        self.header.entity_type = value

    @property
    def entity_id(self) -> int:
        return self.header.entity_id

    @entity_id.setter
    def entity_id(self, value: int) -> None:
        self.header.entity_id = value

    @property
    def data(self) -> Container:
        return self._raw.data

    @data.setter
    def data(self, value: Container) -> None:
        self._raw.data = value

    @property
    def header(self) -> Container:
        return self.data.header

    @header.setter
    def header(self, value: Container) -> None:
        self.data.header = value

    @property
    def position(self) -> Vec3:
        return self.header.position

    @position.setter
    def position(self, value: Vec3) -> None:
        self.header.position = value

    @property
    def up_vector(self) -> Vec3:
        return self.header.up_vector

    @up_vector.setter
    def up_vector(self, value: Vec3) -> None:
        self.header.up_vector = value

    @property
    def facing_vector(self) -> Vec3:
        return self.header.facing_vector

    @facing_vector.setter
    def facing_vector(self, value: Vec3) -> None:
        self.header.facing_vector = value

    @property
    def type_construct(self) -> Struct:
        return types_to_construct[self.entity_type]

    @property
    def size(self) -> int:
        return self.type_construct.sizeof()

    def platform_data(self) -> Platform:
        return Platform(self.data)

    def object_data(self) -> Object:
        return Object(self.data)

    def player_spawn_data(self) -> PlayerSpawn:
        return PlayerSpawn(self.data)

    def door_data(self) -> Door:
        return Door(self.data)

    def item_spawn_data(self) -> ItemSpawn:
        return ItemSpawn(self.data)

    def enemy_spawn_data(self) -> EnemySpawn:
        return EnemySpawn(self.data)

    def trigger_volume_data(self) -> TriggerVolume:
        return TriggerVolume(self.data)

    def area_volume_data(self) -> AreaVolume:
        return AreaVolume(self.data)

    def jump_pad_data(self) -> JumpPad:
        return JumpPad(self.data)

    def point_module_data(self) -> PointModule:
        return PointModule(self.data)

    def morph_camera_data(self) -> MorphCamera:
        return MorphCamera(self.data)

    def octolith_flag_data(self) -> OctolithFlag:
        return OctolithFlag(self.data)

    def flag_base_data(self) -> FlagBase:
        return FlagBase(self.data)

    def teleporter_data(self) -> Teleporter:
        return Teleporter(self.data)

    def defense_node_data(self) -> DefenseNode:
        return DefenseNode(self.data)

    def light_source_data(self) -> LightSource:
        return LightSource(self.data)

    def artifact_data(self) -> Artifact:
        return Artifact(self.data)

    def camera_sequence_data(self) -> CameraSequence:
        return CameraSequence(self.data)

    def force_field_data(self) -> ForceField:
        return ForceField(self.data)


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

    def append_entity(self, template: Any) -> int:
        new_entity_id = self.get_max_entity_id() + 1
        template.entity_id = new_entity_id
        self.entities.append(Entity.create(template))
        return new_entity_id
