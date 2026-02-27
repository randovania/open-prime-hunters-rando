import enum

import construct
from construct import Byte, Construct, Container, Flag, Int16sl, Int16ul, Int32sl, Int32ul, Padded, Struct, Switch

from open_prime_hunters_rando.common import EnumAdapter, FixedPoint
from open_prime_hunters_rando.entities.entity import Entity
from open_prime_hunters_rando.entities.entity_file import (
    DecodedString,
    EntityDataHeader,
    ItemTypeConstruct,
    MessageConstruct,
    Vector3Fx,
)
from open_prime_hunters_rando.entities.entity_types.enemy_spawn_fields.hunter import Hunter
from open_prime_hunters_rando.entities.entity_types.volume_type import RawCollisionVolume
from open_prime_hunters_rando.entities.enum import ItemType, Message


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
    "data" / WarWaspSpawnField,
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
    "sphere1_radius" / FixedPoint,
    "sphere2_position" / Vector3Fx,
    "sphere2_radius" / FixedPoint,
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
    "active_distance" / FixedPoint,
    "enemy_active_distance" / FixedPoint,
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


class EnemySpawn(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return EnemySpawnEntityData

    @property
    def enemy_type(self) -> EnemyType:
        return self._raw.data.enemy_type

    @enemy_type.setter
    def enemy_type(self, value: EnemyType) -> None:
        self._raw.data.enemy_type = value

    @property
    def fields(self) -> Container:
        return self._raw.data.fields

    @fields.setter
    def fields(self, value: Container) -> None:
        self._raw.data.fields = value

    @property
    def linked_entity_id(self) -> int:
        return self._raw.data.linked_entity_id

    @linked_entity_id.setter
    def linked_entity_id(self, value: int) -> None:
        self._raw.data.linked_entity_id = value

    @property
    def spawn_limit(self) -> int:
        return self._raw.data.spawn_limit

    @spawn_limit.setter
    def spawn_limit(self, value: int) -> None:
        self._raw.data.spawn_limit = value

    @property
    def spawn_total(self) -> int:
        return self._raw.data.spawn_total

    @spawn_total.setter
    def spawn_total(self, value: int) -> None:
        self._raw.data.spawn_total = value

    @property
    def spawn_count(self) -> int:
        return self._raw.data.spawn_count

    @spawn_count.setter
    def spawn_count(self, value: int) -> None:
        self._raw.data.spawn_count = value

    @property
    def active(self) -> bool:
        return self._raw.data.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.data.active = value

    @property
    def always_active(self) -> bool:
        return self._raw.data.always_active

    @always_active.setter
    def always_active(self, value: bool) -> None:
        self._raw.data.always_active = value

    @property
    def item_chance(self) -> int:
        return self._raw.data.item_chance

    @item_chance.setter
    def item_chance(self, value: int) -> None:
        self._raw.data.item_chance = value

    @property
    def spawner_health(self) -> int:
        return self._raw.data.spawner_health

    @spawner_health.setter
    def spawner_health(self, value: int) -> None:
        self._raw.data.spawner_health = value

    @property
    def cooldown_time(self) -> int:
        return self._raw.data.cooldown_time

    @cooldown_time.setter
    def cooldown_time(self, value: int) -> None:
        self._raw.data.cooldown_time = value

    @property
    def initial_cooldown(self) -> int:
        return self._raw.data.initial_cooldown

    @initial_cooldown.setter
    def initial_cooldown(self, value: int) -> None:
        self._raw.data.initial_cooldown = value

    @property
    def active_distance(self) -> float:
        return self._raw.data.active_distance

    @active_distance.setter
    def active_distance(self, value: float) -> None:
        self._raw.data.active_distance = value

    @property
    def enemy_active_distance(self) -> float:
        return self._raw.data.enemy_active_distance

    @enemy_active_distance.setter
    def enemy_active_distance(self, value: float) -> None:
        self._raw.data.enemy_active_distance = value

    @property
    def node_name(self) -> str:
        return self._raw.data.node_name

    @node_name.setter
    def node_name(self, value: str) -> None:
        self._raw.data.node_name = value

    @property
    def entity_id1(self) -> int:
        return self._raw.data.entity_id1

    @entity_id1.setter
    def entity_id1(self, value: int) -> None:
        self._raw.data.entity_id1 = value

    @property
    def message1(self) -> Message:
        return self._raw.data.message1

    @message1.setter
    def message1(self, value: Message) -> None:
        self._raw.data.message1 = value

    @property
    def entity_id2(self) -> int:
        return self._raw.data.entity_id2

    @entity_id2.setter
    def entity_id2(self, value: int) -> None:
        self._raw.data.entity_id2 = value

    @property
    def message2(self) -> Message:
        return self._raw.data.message2

    @message2.setter
    def message2(self, value: Message) -> None:
        self._raw.data.message2 = value

    @property
    def entity_id3(self) -> int:
        return self._raw.data.entity_id3

    @entity_id3.setter
    def entity_id3(self, value: int) -> None:
        self._raw.data.entity_id3 = value

    @property
    def message3(self) -> Message:
        return self._raw.data.message3

    @message3.setter
    def message3(self, value: Message) -> None:
        self._raw.data.message3 = value

    @property
    def item_type(self) -> ItemType:
        return self._raw.data.item_type

    @item_type.setter
    def item_type(self, value: ItemType) -> None:
        self._raw.data.item_type = value
