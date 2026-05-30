import typing

from construct import Byte, Construct, Flag, Int16sl, Int16ul, Int32sl, Int32ul, Padded, Struct

from open_prime_hunters_rando.parsing.common_types import (
    BaseFlags,
    DecodedString,
    FixedPoint,
    ItemTypeConstruct,
    MessageConstruct,
)
from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vec4, Vector3Fx, Vector4Fx
from open_prime_hunters_rando.parsing.construct_extensions import FlagsEnumAdapter
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType, ItemType, Message


class PlatformFlags(BaseFlags):
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


PlatformFlagsConstruct: FlagsEnumAdapter = FlagsEnumAdapter(PlatformFlags, Int32ul)


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
    "platform_flags" / PlatformFlagsConstruct,
    "contact_damage" / Int32ul,
    "beam_spawn_direction" / Vector3Fx,
    "beam_spawn_position" / Vector3Fx,
    "beam_id" / Int32sl,
    "beam_interval" / Int32ul,
    "beam_on_intervals" / Int32ul,
    "field27" / Int16ul,  # Unused
    "field28" / Int16ul,  # Unused
    "resist_effect_id" / Int32sl,
    "health" / Int32ul,
    "effectiveness" / Int32ul,
    "damage_effect_id" / Int32sl,
    "dead_effect_id" / Int32sl,
    "item_chance" / Padded(4, Byte),
    "item_type" / ItemTypeConstruct,
    "field36" / Int32ul,  # Unused
    "field37" / Int32ul,  # Unused
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

    forward_speed = field(float)
    backward_speed = field(float)

    portal_name = field(str)

    movement_type = field(int)
    for_cutscene = field(int)
    reverse_type = field(int)

    platform_flags = field(PlatformFlags)

    contact_damage = field(int)

    beam_spawn_direction = field(Vec3)
    beam_spawn_position = field(Vec3)
    beam_id = field(int)
    beam_interval = field(int)
    beam_on_intervals = field(int)

    field27 = field(int)
    field28 = field(int)

    resist_effect_id = field(int)

    health = field(int)
    effectiveness = field(int)

    damage_effect_id = field(int)
    dead_effect_id = field(int)

    item_chance = field(int)
    item_type = field(ItemType)

    field36 = field(int)
    field37 = field(int)

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

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.PLATFORM

    @classmethod
    def create(
        cls,
        node_name: str = "",
        layer_state: typing.Sequence[bool] = (False,) * 16,
        entity_id: int = -1,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 1.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 1.0),
        no_port: int = 1,
        model_id: int = 0,
        parent_id: int = -1,
        active: bool = True,
        delay: int = 150,
        scan_data1: int = 0,
        scan_message_target: int = -1,
        scan_message: Message = Message.NONE,
        scan_data2: int = 0,
        position_count: int = 0,
        positions: list[Vec3 | tuple[float, float, float]] = [Vec3(0.0, 0.0, 0.0)] * 10,
        rotations: list[Vec4 | tuple[float, float, float, float]] = [(0.0, 0.0, 0.0, 0.0)] * 10,
        position_offset: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        forward_speed: float = 0.0,
        backward_speed: float = 0.0,
        portal_name: str = "",
        movement_type: int = 0,
        for_cutscene: int = 0,
        reverse_type: int = 1,
        platform_flags: PlatformFlags = PlatformFlags.NONE,
        contact_damage: int = 1,
        beam_spawn_direction: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        beam_spawn_position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        beam_id: int = 0,
        beam_interval: int = 10,
        beam_on_intervals: int = 1,
        field27: int = 65535,
        field28: int = 0,
        resist_effect_id: int = 0,
        health: int = 100,
        effectiveness: int = 1,
        damage_effect_id: int = 0,
        dead_effect_id: int = 0,
        item_chance: int = 100,
        item_type: ItemType = ItemType.NONE,
        field36: int = 0,
        field37: int = 4294967295,
        beam_hit_message_target: int = 65535,
        beam_hit_message: Message = Message.NONE,
        beam_hit_message_param1: int = 0,
        beam_hit_message_param2: int = 0,
        player_collision_message_target: int = 65535,
        player_collision_message: Message = Message.NONE,
        player_collision_message_param1: int = 0,
        player_collision_message_param2: int = 0,
        dead_message_target: int = 65635,
        dead_message: Message = Message.NONE,
        dead_message_param1: int = 0,
        dead_message_param2: int = 0,
        lifetime_message1_index: int = 255,
        lifetime_message1_target: int = -1,
        lifetime_message1: Message = Message.NONE,
        lifetime_message1_param1: int = 0,
        lifetime_message1_param2: int = 0,
        lifetime_message2_index: int = 255,
        lifetime_message2_target: int = -1,
        lifetime_message2: Message = Message.NONE,
        lifetime_message2_param1: int = 0,
        lifetime_message2_param2: int = 0,
        lifetime_message3_index: int = 255,
        lifetime_message3_target: int = -1,
        lifetime_message3: Message = Message.NONE,
        lifetime_message3_param1: int = 0,
        lifetime_message3_param2: int = 0,
        lifetime_message4_index: int = 255,
        lifetime_message4_target: int = -1,
        lifetime_message4: Message = Message.NONE,
        lifetime_message4_param1: int = 0,
        lifetime_message4_param2: int = 0,
    ) -> typing.Self:
        obj = super().create(
            node_name,
            layer_state,
            entity_id,
            position,
            up_vector,
            facing_vector,
        )
        obj.no_port = no_port
        obj.model_id = model_id
        obj.parent_id = parent_id
        obj.active = active
        obj.delay = delay
        obj.scan_data1 = scan_data1
        obj.scan_message_target = scan_message_target
        obj.scan_message = scan_message
        obj.scan_data2 = scan_data2
        obj.position_count = position_count
        obj.positions = [Vec3(*position) for position in positions]
        obj.rotations = [Vec4(*rotation) for rotation in rotations]
        obj.position_offset = Vec3(*position_offset)
        obj.forward_speed = forward_speed
        obj.backward_speed = backward_speed
        obj.portal_name = portal_name
        obj.movement_type = movement_type
        obj.for_cutscene = for_cutscene
        obj.reverse_type = reverse_type
        obj.platform_flags = platform_flags
        obj.active = active
        obj.contact_damage = contact_damage
        obj.beam_spawn_direction = Vec3(*beam_spawn_direction)
        obj.beam_spawn_position = Vec3(*beam_spawn_position)
        obj.beam_id = beam_id
        obj.beam_interval = beam_interval
        obj.beam_on_intervals = beam_on_intervals
        obj.field27 = field27
        obj.field28 = field28
        obj.resist_effect_id = resist_effect_id
        obj.health = health
        obj.effectiveness = effectiveness
        obj.damage_effect_id = damage_effect_id
        obj.dead_effect_id = dead_effect_id
        obj.item_chance = item_chance
        obj.item_type = item_type
        obj.field36 = field36
        obj.field37 = field37
        obj.beam_hit_message_target = beam_hit_message_target
        obj.beam_hit_message = beam_hit_message
        obj.beam_hit_message_param1 = beam_hit_message_param1
        obj.beam_hit_message_param2 = beam_hit_message_param2
        obj.player_collision_message_target = player_collision_message_target
        obj.player_collision_message = player_collision_message
        obj.player_collision_message_param1 = player_collision_message_param1
        obj.player_collision_message_param2 = player_collision_message_param2
        obj.dead_message_target = dead_message_target
        obj.dead_message = dead_message
        obj.dead_message_param1 = dead_message_param1
        obj.dead_message_param2 = dead_message_param2
        obj.lifetime_message1_index = lifetime_message1_index
        obj.lifetime_message1_target = lifetime_message1_target
        obj.lifetime_message1 = lifetime_message1
        obj.lifetime_message1_param1 = lifetime_message1_param1
        obj.lifetime_message1_param2 = lifetime_message1_param2
        obj.lifetime_message2_index = lifetime_message2_index
        obj.lifetime_message2_target = lifetime_message2_target
        obj.lifetime_message2 = lifetime_message2
        obj.lifetime_message2_param1 = lifetime_message2_param1
        obj.lifetime_message2_param2 = lifetime_message2_param2
        obj.lifetime_message3_index = lifetime_message3_index
        obj.lifetime_message3_target = lifetime_message3_target
        obj.lifetime_message3 = lifetime_message3
        obj.lifetime_message3_param1 = lifetime_message3_param1
        obj.lifetime_message3_param2 = lifetime_message3_param2
        obj.lifetime_message4_index = lifetime_message4_index
        obj.lifetime_message4_target = lifetime_message4_target
        obj.lifetime_message4 = lifetime_message4
        obj.lifetime_message4_param1 = lifetime_message4_param1
        obj.lifetime_message4_param2 = lifetime_message4_param2

        return obj
