import enum

import construct
from construct import (
    Byte,
    Construct,
    Flag,
    Int16sl,
    Int16ul,
    Int32sl,
    Int32ul,
    Struct,
)

from open_prime_hunters_rando.common import FixedPoint, Vec3, Vec4
from open_prime_hunters_rando.entities.entity import Entity
from open_prime_hunters_rando.entities.entity_file import (
    DecodedString,
    EntityDataHeader,
    ItemTypeConstruct,
    MessageConstruct,
    Vector3Fx,
    Vector4Fx,
)
from open_prime_hunters_rando.entities.enum import ItemType, Message


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


class Platform(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return PlatformEntityData

    @property
    def no_port(self) -> int:
        return self._raw.data.data.no_port

    @no_port.setter
    def no_port(self, value: int) -> None:
        self._raw.data.data.no_port = value

    @property
    def model_id(self) -> int:
        return self._raw.data.data.model_id

    @model_id.setter
    def model_id(self, value: int) -> None:
        self._raw.data.data.model_id = value

    @property
    def parent_id(self) -> int:
        return self._raw.data.data.parent_id

    @parent_id.setter
    def parent_id(self, value: int) -> None:
        self._raw.data.data.parent_id = value

    @property
    def active(self) -> bool:
        return self._raw.data.data.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.data.data.active = value

    @property
    def delay(self) -> int:
        return self._raw.data.data.delay

    @delay.setter
    def delay(self, value: int) -> None:
        self._raw.data.data.delay = value

    @property
    def scan_data1(self) -> int:
        return self._raw.data.data.scan_data1

    @scan_data1.setter
    def scan_data1(self, value: int) -> None:
        self._raw.data.data.scan_data1 = value

    @property
    def scan_message_target(self) -> int:
        return self._raw.data.data.scan_message_target

    @scan_message_target.setter
    def scan_message_target(self, value: int) -> None:
        self._raw.data.data.scan_message_target = value

    @property
    def scan_message(self) -> Message:
        return self._raw.data.data.scan_message

    @scan_message.setter
    def scan_message(self, value: Message) -> None:
        self._raw.data.data.scan_message = value

    @property
    def scan_data2(self) -> int:
        return self._raw.data.data.scan_data2

    @scan_data2.setter
    def scan_data2(self, value: int) -> None:
        self._raw.data.data.scan_data2 = value

    @property
    def position_count(self) -> int:
        return self._raw.data.data.position_count

    @position_count.setter
    def position_count(self, value: int) -> None:
        self._raw.data.data.position_count = value

    @property
    def positions(self) -> list[Vec3]:
        return self._raw.data.data.positions

    @positions.setter
    def positions(self, value: list[Vec3]) -> None:
        self._raw.data.data.positions = value

    @property
    def rotations(self) -> list[Vec4]:
        return self._raw.data.data.rotations

    @rotations.setter
    def rotations(self, value: list[Vec4]) -> None:
        self._raw.data.data.rotations = value

    @property
    def position_offset(self) -> Vec3:
        return self._raw.data.data.position_offset

    @position_offset.setter
    def position_offset(self, value: Vec3) -> None:
        self._raw.data.data.position_offset = value

    @property
    def forward_speed(self) -> int:
        return self._raw.data.data.forward_speed

    @forward_speed.setter
    def forward_speed(self, value: float) -> None:
        self._raw.data.data.forward_speed = value

    @property
    def backward_speed(self) -> float:
        return self._raw.data.data.backward_speed

    @backward_speed.setter
    def backward_speed(self, value: float) -> None:
        self._raw.data.data.backward_speed = value

    @property
    def portal_name(self) -> str:
        return self._raw.data.data.portal_name

    @portal_name.setter
    def portal_name(self, value: str) -> None:
        self._raw.data.data.portal_name = value

    @property
    def movement_type(self) -> int:
        return self._raw.data.data.movement_type

    @movement_type.setter
    def movement_type(self, value: int) -> None:
        self._raw.data.data.movement_type = value

    @property
    def for_cutscene(self) -> int:
        return self._raw.data.data.for_cutscene

    @for_cutscene.setter
    def for_cutscene(self, value: int) -> None:
        self._raw.data.data.for_cutscene = value

    @property
    def reverse_type(self) -> int:
        return self._raw.data.data.reverse_type

    @reverse_type.setter
    def reverse_type(self, value: int) -> None:
        self._raw.data.data.reverse_type = value

    def flags(self, flag: PlatformFlags) -> bool:
        return self._raw.data.flags[flag.name]

    def set_flags(self, flag: PlatformFlags, state: bool) -> None:
        self._raw.data.effect_flags[flag.name] = state

    @property
    def contact_damage(self) -> int:
        return self._raw.data.data.contact_damage

    @contact_damage.setter
    def contact_damage(self, value: int) -> None:
        self._raw.data.data.contact_damage = value

    @property
    def beam_spawn_direction(self) -> Vec3:
        return self._raw.data.data.beam_spawn_direction

    @beam_spawn_direction.setter
    def beam_spawn_direction(self, value: Vec3) -> None:
        self._raw.data.data.beam_spawn_direction = value

    @property
    def beam_spawn_position(self) -> Vec3:
        return self._raw.data.data.beam_spawn_position

    @beam_spawn_position.setter
    def beam_spawn_position(self, value: Vec3) -> None:
        self._raw.data.data.beam_spawn_position = value

    @property
    def beam_id(self) -> int:
        return self._raw.data.data.beam_id

    @beam_id.setter
    def beam_id(self, value: int) -> None:
        self._raw.data.data.beam_id = value

    @property
    def beam_interval(self) -> int:
        return self._raw.data.data.beam_interval

    @beam_interval.setter
    def beam_interval(self, value: int) -> None:
        self._raw.data.data.beam_interval = value

    @property
    def beam_on_intervals(self) -> int:
        return self._raw.data.data.beam_on_intervals

    @beam_on_intervals.setter
    def beam_on_intervals(self, value: int) -> None:
        self._raw.data.data.beam_on_intervals = value

    @property
    def resist_effect_id(self) -> int:
        return self._raw.data.data.resist_effect_id

    @resist_effect_id.setter
    def resist_effect_id(self, value: int) -> None:
        self._raw.data.data.resist_effect_id = value

    @property
    def health(self) -> int:
        return self._raw.data.data.health

    @health.setter
    def health(self, value: int) -> None:
        self._raw.data.data.health = value

    @property
    def effectiveness(self) -> int:
        return self._raw.data.data.effectiveness

    @effectiveness.setter
    def effectiveness(self, value: int) -> None:
        self._raw.data.data.effectiveness = value

    @property
    def damage_effect_id(self) -> int:
        return self._raw.data.data.damage_effect_id

    @damage_effect_id.setter
    def damage_effect_id(self, value: int) -> None:
        self._raw.data.data.damage_effect_id = value

    @property
    def dead_effect_id(self) -> int:
        return self._raw.data.data.dead_effect_id

    @dead_effect_id.setter
    def dead_effect_id(self, value: int) -> None:
        self._raw.data.data.dead_effect_id = value

    @property
    def item_chance(self) -> int:
        return self._raw.data.data.item_chance

    @item_chance.setter
    def item_chance(self, value: int) -> None:
        self._raw.data.data.item_chance = value

    @property
    def item_type(self) -> ItemType:
        return self._raw.data.data.item_type

    @item_type.setter
    def item_type(self, value: ItemType) -> None:
        self._raw.data.data.item_type = value

    @property
    def beam_hit_message_target(self) -> int:
        return self._raw.data.data.beam_hit_message_target

    @beam_hit_message_target.setter
    def beam_hit_message_target(self, value: int) -> None:
        self._raw.data.data.beam_hit_message_target = value

    @property
    def beam_hit_message(self) -> Message:
        return self._raw.data.data.beam_hit_message

    @beam_hit_message.setter
    def beam_hit_message(self, value: Message) -> None:
        self._raw.data.data.beam_hit_message = value

    @property
    def beam_hit_message_param1(self) -> int:
        return self._raw.data.data.beam_hit_message_param1

    @beam_hit_message_param1.setter
    def beam_hit_message_param1(self, value: int) -> None:
        self._raw.data.data.beam_hit_message_param1 = value

    @property
    def beam_hit_message_param2(self) -> int:
        return self._raw.data.data.beam_hit_message_param2

    @beam_hit_message_param2.setter
    def beam_hit_message_param2(self, value: int) -> None:
        self._raw.data.data.beam_hit_message_param2 = value

    @property
    def player_collision_message_target(self) -> int:
        return self._raw.data.data.player_collision_message_target

    @player_collision_message_target.setter
    def player_collision_message_target(self, value: int) -> None:
        self._raw.data.data.player_collision_message_target = value

    @property
    def player_collision_message(self) -> Message:
        return self._raw.data.data.player_collision_message

    @player_collision_message.setter
    def player_collision_message(self, value: Message) -> None:
        self._raw.data.data.player_collision_message = value

    @property
    def player_collision_message_param1(self) -> int:
        return self._raw.data.data.player_collision_message_param1

    @player_collision_message_param1.setter
    def player_collision_message_param1(self, value: int) -> None:
        self._raw.data.data.player_collision_message_param1 = value

    @property
    def player_collision_message_param2(self) -> int:
        return self._raw.data.data.player_collision_message_param2

    @player_collision_message_param2.setter
    def player_collision_message_param2(self, value: int) -> None:
        self._raw.data.data.player_collision_message_param2 = value

    @property
    def dead_message_target(self) -> int:
        return self._raw.data.data.dead_message_target

    @dead_message_target.setter
    def dead_message_target(self, value: int) -> None:
        self._raw.data.data.dead_message_target = value

    @property
    def dead_message(self) -> Message:
        return self._raw.data.data.dead_message

    @dead_message.setter
    def dead_message(self, value: Message) -> None:
        self._raw.data.data.dead_message = value

    @property
    def dead_message_param1(self) -> int:
        return self._raw.data.data.dead_message_param1

    @dead_message_param1.setter
    def dead_message_param1(self, value: int) -> None:
        self._raw.data.data.dead_message_param1 = value

    @property
    def dead_message_param2(self) -> int:
        return self._raw.data.data.dead_message_param2

    @dead_message_param2.setter
    def dead_message_param2(self, value: int) -> None:
        self._raw.data.data.dead_message_param2 = value

    @property
    def lifetime_message1_index(self) -> int:
        return self._raw.data.data.lifetime_message1_target

    @property
    def lifetime_message1_target(self) -> int:
        return self._raw.data.data.lifetime_message1_target

    @lifetime_message1_target.setter
    def lifetime_message1_target(self, value: int) -> None:
        self._raw.data.data.lifetime_message1_target = value

    @property
    def lifetime_message1(self) -> Message:
        return self._raw.data.data.lifetime_message1

    @lifetime_message1.setter
    def lifetime_message1(self, value: Message) -> None:
        self._raw.data.data.lifetime_message1 = value

    @property
    def lifetime_message1_param1(self) -> int:
        return self._raw.data.data.lifetime_message1_param1

    @lifetime_message1_param1.setter
    def lifetime_message1_param1(self, value: int) -> None:
        self._raw.data.data.lifetime_message1_param1 = value

    @property
    def lifetime_message1_param2(self) -> int:
        return self._raw.data.data.lifetime_message1_param2

    @lifetime_message1_param2.setter
    def lifetime_message1_param2(self, value: int) -> None:
        self._raw.data.data.lifetime_message1_param2 = value

    @property
    def lifetime_message2_index(self) -> int:
        return self._raw.data.data.lifetime_message2_target

    @property
    def lifetime_message2_target(self) -> int:
        return self._raw.data.data.lifetime_message2_target

    @lifetime_message2_target.setter
    def lifetime_message2_target(self, value: int) -> None:
        self._raw.data.data.lifetime_message2_target = value

    @property
    def lifetime_message2(self) -> Message:
        return self._raw.data.data.lifetime_message2

    @lifetime_message2.setter
    def lifetime_message2(self, value: Message) -> None:
        self._raw.data.data.lifetime_message2 = value

    @property
    def lifetime_message2_param1(self) -> int:
        return self._raw.data.data.lifetime_message2_param1

    @lifetime_message2_param1.setter
    def lifetime_message2_param1(self, value: int) -> None:
        self._raw.data.data.lifetime_message2_param1 = value

    @property
    def lifetime_message2_param2(self) -> int:
        return self._raw.data.data.lifetime_message2_param2

    @lifetime_message2_param2.setter
    def lifetime_message2_param2(self, value: int) -> None:
        self._raw.data.data.lifetime_message2_param2 = value

    @property
    def lifetime_message3_index(self) -> int:
        return self._raw.data.data.lifetime_message3_target

    @property
    def lifetime_message3_target(self) -> int:
        return self._raw.data.data.lifetime_message3_target

    @lifetime_message3_target.setter
    def lifetime_message3_target(self, value: int) -> None:
        self._raw.data.data.lifetime_message3_target = value

    @property
    def lifetime_message3(self) -> Message:
        return self._raw.data.data.lifetime_message3

    @lifetime_message3.setter
    def lifetime_message3(self, value: Message) -> None:
        self._raw.data.data.lifetime_message3 = value

    @property
    def lifetime_message3_param1(self) -> int:
        return self._raw.data.data.lifetime_message3_param1

    @lifetime_message3_param1.setter
    def lifetime_message3_param1(self, value: int) -> None:
        self._raw.data.data.lifetime_message3_param1 = value

    @property
    def lifetime_message3_param2(self) -> int:
        return self._raw.data.data.lifetime_message3_param2

    @lifetime_message3_param2.setter
    def lifetime_message3_param2(self, value: int) -> None:
        self._raw.data.data.lifetime_message3_param2 = value

    @property
    def lifetime_message4_index(self) -> int:
        return self._raw.data.data.lifetime_message4_target

    @property
    def lifetime_message4_target(self) -> int:
        return self._raw.data.data.lifetime_message4_target

    @lifetime_message4_target.setter
    def lifetime_message4_target(self, value: int) -> None:
        self._raw.data.data.lifetime_message4_target = value

    @property
    def lifetime_message4(self) -> Message:
        return self._raw.data.data.lifetime_message4

    @lifetime_message4.setter
    def lifetime_message4(self, value: Message) -> None:
        self._raw.data.data.lifetime_message4 = value

    @property
    def lifetime_message4_param1(self) -> int:
        return self._raw.data.data.lifetime_message4_param1

    @lifetime_message4_param1.setter
    def lifetime_message4_param1(self, value: int) -> None:
        self._raw.data.data.lifetime_message4_param1 = value

    @property
    def lifetime_message4_param2(self) -> int:
        return self._raw.data.data.lifetime_message4_param2

    @lifetime_message4_param2.setter
    def lifetime_message4_param2(self, value: int) -> None:
        self._raw.data.data.lifetime_message4_param2 = value
