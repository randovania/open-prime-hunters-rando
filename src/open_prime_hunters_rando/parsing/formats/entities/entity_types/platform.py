import enum

import construct
from construct import Byte, Construct, Flag, Int16sl, Int16ul, Int32sl, Int32ul, Padded, Struct

from open_prime_hunters_rando.parsing.common_types import DecodedString, FixedPoint, ItemTypeConstruct, MessageConstruct
from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vec4, Vector3Fx, Vector4Fx
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.enum import ItemType, Message


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


PlatformEntityData = Struct(
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
    "forward_speed" / FixedPoint,
    "backward_speed" / FixedPoint,
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
    "item_chance" / Padded(4, Byte),
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


class Platform(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return PlatformEntityData

    no_port = field(int)

    model_id = field(int)
    parent_id = field(int)

    active = field(bool)

    delay = field(int)

    scan_data1 = field(int)
    scan_message_target = field(int)
    scan_message = field(Message)
    scan_data2 = field(int)

    position_count = field(int)
    positions = field(list[Vec3])
    rotations = field(list[Vec4])
    position_offset = field(Vec3)

    forward_speed = field(int)
    backward_speed = field(int)

    portal_name = field(str)

    movement_type = field(int)
    for_cutscene = field(int)
    reverse_type = field(int)

    flags = field(dict[PlatformFlags, bool])

    contact_damage = field(int)

    beam_spawn_direction = field(Vec3)
    beam_spawn_position = field(Vec3)
    beam_id = field(int)
    beam_interval = field(int)
    beam_on_intervals = field(int)

    resist_effect_id = field(int)

    health = field(int)
    effectiveness = field(int)

    damage_effect_id = field(int)
    dead_effect_id = field(int)

    item_chance = field(int)
    item_type = field(ItemType)

    beam_hit_message_target = field(int)
    beam_hit_message = field(Message)
    beam_hit_message_param1 = field(int)
    beam_hit_message_param2 = field(int)

    player_collision_message_target = field(int)
    player_collision_message = field(Message)
    player_collision_message_param1 = field(int)
    player_collision_message_param2 = field(int)

    dead_message_target = field(int)
    dead_message = field(Message)
    dead_message_param1 = field(int)
    dead_message_param2 = field(int)

    lifetime_message1_index = field(int)
    lifetime_message1_target = field(int)
    lifetime_message1 = field(Message)
    lifetime_message1_param1 = field(int)
    lifetime_message1_param2 = field(int)

    lifetime_message2_index = field(int)
    lifetime_message2_target = field(int)
    lifetime_message2 = field(Message)
    lifetime_message2_param1 = field(int)
    lifetime_message2_param2 = field(int)

    lifetime_message3_index = field(int)
    lifetime_message3_target = field(int)
    lifetime_message3 = field(Message)
    lifetime_message3_param1 = field(int)
    lifetime_message3_param2 = field(int)

    lifetime_message4_index = field(int)
    lifetime_message4_target = field(int)
    lifetime_message4 = field(Message)
    lifetime_message4_param1 = field(int)
    lifetime_message4_param2 = field(int)
