import enum
import math

import construct
from construct import (
    Byte,
    Flag,
    Int16sl,
    Int16ul,
    Int32sl,
    Int32ul,
    PaddedString,
    Peek,
    Pointer,
    RepeatUntil,
    StopIf,
    Struct,
    Switch,
    this,
)


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


EntityTypeConstruct = construct.Enum(Int16ul, EntityType)


class FixedAdapter(construct.Adapter):
    """Fixed-point number with 12-bit fractional part"""

    def __init__(self) -> None:
        super().__init__(construct.Int32ul)

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

DecodedString = PaddedString(16, "utf-8")

EntityDataHeader = Struct(
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


MessageConstruct = construct.Enum(Int32ul, Message)

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
    "unk" / Int32ul[4],
    "portal_name" / DecodedString,
    "movment_type" / Int32ul,
    "for_cutscene" / Int32ul,
    "reverse_type" / Int32ul,
    "flags" / Int32ul,
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
    "item_type" / Int32sl,
    "_unused3" / Int32ul,
    "_unused4" / Int32ul,
    "beam_hit_message_target" / Int32sl,
    "beam_hit_message" / MessageConstruct,
    "beam_hit_message_param1" / Int32sl,
    "beam_hit_message_param2" / Int32sl,
    "dead_message_target" / Int32sl,
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
    "type" / construct.Enum(Int32ul, VolumeType),
    "data" / Switch(construct.this.type, volume_types),
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


DoorEntityData = Struct(
    "header" / EntityDataHeader,
    "node_name" / DecodedString,
    "palette_id" / Int32ul,
    "door_type" / construct.Enum(Int32ul, DoorType),
    "connector_id" / Int32ul,
    "target_layer_id" / Byte,
    "locked" / Flag,
    "out_connector_id" / Byte,
    "out_loader_id" / Byte,
    "entity_file_name" / DecodedString,
    "room_name" / DecodedString,
)


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


ItemTypeConstruct = construct.Enum(Int32ul, ItemType)


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
    "collected_message_param1" / Int16ul,
    "collected_message_param2" / Int16ul,
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


enemy_spawn_fields = {
    (
        EnemyType.ZOOMER
        or EnemyType.GEEMER
        or EnemyType.BLASTCAP
        or EnemyType.VOLDRUM2
        or EnemyType.QUADTROID
        or EnemyType.CRASH_PILLAR
        or EnemyType.SLENCH
        or EnemyType.LESSER_ITHRAK
        or EnemyType.TROCRA
    ): Struct(
        "volume0" / RawCollisionVolume,
        "volume1" / RawCollisionVolume,
        "volume2" / RawCollisionVolume,
        "volume3" / RawCollisionVolume,
        "_empty_bytes" / Int32ul[36],
    ),
    EnemyType.WAR_WASP: Struct(
        "war_wasp" / WarWaspSpawnField,
        "_padding1" / Int16ul,
        "_padding2" / Int16ul,
    ),
    EnemyType.SHRIEKBAT: Struct(
        "volume0" / RawCollisionVolume,
        "path_vector" / Vector3Fx,
        "volume1" / RawCollisionVolume,
        "volume2" / RawCollisionVolume,
        "_empty_bytes" / Int32ul[49],
    ),
    EnemyType.BARBED_WAR_WASP: Struct(
        "enemy_subtype" / Int32ul,
        "enemy_version" / Int32ul,
        "war_wasp" / WarWaspSpawnField,
    ),
    (EnemyType.TEMROID or EnemyType.PETRASYL1): Struct(
        "volume0" / RawCollisionVolume,
        "_unused" / Int32ul[7],
        "facing" / Vector3Fx,
        "position" / Vector3Fx,
        "idle_range" / Vector3Fx,
        "_empty_bytes" / Int32ul[68],
    ),
    (EnemyType.PETRASYL2 or EnemyType.PETRASYL3 or EnemyType.PETRASYL4): Struct(
        "volume0" / RawCollisionVolume,
        "_unused" / Int32ul[4],
        "position" / Vector3Fx,
        "weave_offset" / Int32ul,
        "field" / Int32sl,
        "_empty_bytes" / Int32ul[75],
    ),
    (EnemyType.CRETAPHID or EnemyType.GREATER_ITHRAK): Struct(
        "enemy_subtype" / Int32ul,
        "volume0" / RawCollisionVolume,
        "volume1" / RawCollisionVolume,
        "volume2" / RawCollisionVolume,
        "volume3" / RawCollisionVolume,
        "_empty_bytes" / Int32ul[35],
    ),
    (
        EnemyType.ALIMBIC_TURRET
        or EnemyType.PSYCHO_BIT1
        or EnemyType.PSYCHO_BIT2
        or EnemyType.VOLDRUM1
        or EnemyType.FIRE_SPAWN
    ): Struct(
        "enemy_subtype" / Int32ul,
        "enemy_version" / Int32ul,
        "volume0" / RawCollisionVolume,
        "volume1" / RawCollisionVolume,
        "volume2" / RawCollisionVolume,
        "volume3" / RawCollisionVolume,
        "_empty_bytes" / Int32ul[34],
    ),
    EnemyType.CARNIVOROUS_PLANT: Struct(
        "enemy_health" / Int16ul,
        "enemy_damage" / Int16ul,
        "enemy_subtype" / Int32ul,
        "volume0" / RawCollisionVolume,
        "_empty_bytes" / Int32ul[82],
    ),
    EnemyType.HUNTER: Struct(
        "hunter_id" / Int32ul,
        "encounter_type" / Int32ul,
        "hunter_weapon" / Int32ul,
        "hunter_health" / Int16ul,
        "hunter_health_max" / Int16ul,
        "field" / Int16ul,  # set in AI data
        "hunter_color" / Byte,
        "hunter_chance" / Byte,
        "_empty_bytes" / Int32ul[95],
    ),
    EnemyType.SLENCH_TURRET: Struct(
        "enemy_subtype" / Int32ul,
        "enemy_version" / Int32ul,
        "volume0" / RawCollisionVolume,
        "volume1" / RawCollisionVolume,
        "index" / Int32sl,
        "_empty_bytes" / Int32ul[65],
    ),
    EnemyType.GOREA1_A: Struct(
        "sphere1_position" / Vector3Fx,
        "sphere1_radius" / Fixed,
        "sphere2_position" / Vector3Fx,
        "sphere2_radius" / Fixed,
        "_empty_bytes" / Int32ul[92],
    ),
    EnemyType.GOREA2: Struct(
        "field1" / Vector3Fx,
        "field2" / Int32ul,
        "field3" / Int32ul,
        "_empty_bytes" / Int32ul[95],
    ),
}

EnumSpawnUnion = Struct(
    "type" / construct.Enum(Byte, EnemyType),
    "data" / Switch(construct.this.type, enemy_spawn_fields),
)


EnemySpawnEntityData = Struct(
    "header" / EntityDataHeader,
    "enemy_type" / construct.Enum(Byte, EnemyType),
    "_padding1" / Byte,
    "_padding2" / Int16ul,
    "fields" / EnumSpawnUnion,
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
    MAGMAUL = 0x20
    SHOCK_COIL = 0x40
    BEAM_CHARGED = 0x100
    PLAYER_BIPED = 0x200
    PLAYER_ALT = 0x400
    BIT_11 = 0x800  # unused
    INCLUDE_BOTS = 0x1000


TriggerVolumeFlagsConstruct = construct.FlagsEnum(Int32ul, TriggerVolumeFlags)

TriggerVolumeEntityData = Struct(
    "header" / EntityDataHeader,
    "subtype" / construct.Enum(Int32ul, TriggerVolumeType),
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


class AreaVolumeType(enum.Enum):
    VOLUME = 0
    THRESHOLD = 1
    RELAY = 2
    AUTOMATIC = 3
    STATE_BITS = 4


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
    "parent_id" / Int16sl,
    "_unused" / Int16ul,
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
    "entity_filename" / DecodedString,
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
        super().__init__(construct.Int32ul)

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
    "message1_target" / MessageConstruct,
    "_padding1" / Int16ul,
    "message1" / Int16ul,
    "message2_target" / MessageConstruct,
    "_padding2" / Int16ul,
    "message2" / Int16ul,
    "message3_target" / MessageConstruct,
    "_padding3" / Int16ul,
    "message3" / Int16ul,
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
    "type" / Int16ul,
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

EntityEntry = Struct(
    "node_name" / DecodedString,
    "layer_mask" / Int16ul,  # maybe a FlagsEnum? or an array of 16 bools? might not be necessary
    "length" / Int16ul,  # likely needs a Rebuild
    "data_offset" / Int32ul,  # likely needs a Rebuild
    StopIf(this.data_offset == 0),
    "entity_type" / Peek(Pointer(this.data_offset, EntityTypeConstruct)),
    "data" / Pointer(this.data_offset, Switch(this.entity_type, types_to_construct)),
)

EntityFile = Struct(
    "header"
    / Struct(
        "version" / Int32ul,
        "lengths" / Int16ul[16],  # might need a Rebuild?
    ),
    "entities" / RepeatUntil(lambda entity: entity.data_offset == 0, EntityEntry),
)
