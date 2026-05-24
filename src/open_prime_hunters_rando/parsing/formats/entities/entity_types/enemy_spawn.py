import typing

import construct
from construct import (
    Byte,
    Construct,
    Container,
    Flag,
    Int16sl,
    Int16ul,
    Padded,
    Struct,
    Switch,
)

from open_prime_hunters_rando.parsing.common_types import DecodedString, FixedPoint, ItemTypeConstruct, MessageConstruct
from open_prime_hunters_rando.parsing.common_types.vectors import Vec3
from open_prime_hunters_rando.parsing.construct_extensions import EnumAdapter
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies import (
    enemy_type_to_class,
    enemy_type_to_construct,
)
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields, EnemyType
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.hunter import Hunter
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType, ItemType, Message

EnemyTypeConstruct = EnumAdapter(EnemyType, Byte)


EnemySpawnEntityData = Struct(
    "enemy_type" / Padded(4, EnemyTypeConstruct),
    "enemy_fields_raw" / Padded(400, Switch(construct.this.enemy_type, enemy_type_to_construct)),
    "linked_entity_id" / Int16sl,
    "spawn_limit" / Byte,
    "spawn_total" / Byte,
    "spawn_count" / Byte,
    "active" / Flag,
    "always_active" / Flag,
    "item_chance" / Byte,
    "spawner_health" / Int16ul,
    "cooldown_time" / Int16ul,
    "initial_cooldown" / Padded(4, Int16ul),
    "active_distance" / FixedPoint,
    "enemy_active_distance" / FixedPoint,
    "enemy_node_name" / DecodedString,
    "message1_target" / Padded(4, Int16sl),
    "message1" / MessageConstruct,
    "message2_target" / Padded(4, Int16sl),
    "message2" / MessageConstruct,
    "message3_target" / Padded(4, Int16sl),
    "message3" / MessageConstruct,
    "item_type" / ItemTypeConstruct,
)


class EnemySpawn(Entity):
    def __init__(self, raw: Container) -> None:
        super().__init__(raw)
        self._enemy_fields: EnemyFields | None = None

    @classmethod
    def type_construct(cls) -> Construct:
        return EnemySpawnEntityData

    enemy_type = field(EnemyType)

    enemy_fields_raw = field(Container)

    @property
    def enemy_fields(self) -> EnemyFields:
        if self._enemy_fields is None:
            self._enemy_fields = enemy_type_to_class[self.enemy_type](self.enemy_fields_raw)
        return self._enemy_fields

    @enemy_fields.setter
    def enemy_fields(self, value: EnemyFields) -> None:
        self.enemy_fields_raw = value._raw
        self._enemy_fields = value

    linked_entity_id = field(int)

    spawn_limit = field(int)
    spawn_total = field(int)
    spawn_count = field(int)

    active = field(bool)
    always_active = field(bool)

    item_chance = field(int)

    spawner_health = field(int)

    cooldown_time = field(int)
    initial_cooldown = field(int)

    active_distance = field(float)
    enemy_active_distance = field(float)

    enemy_node_name = field(str)

    message1_target = field(int)
    message1 = field(Message)

    message2_target = field(int)
    message2 = field(Message)

    message3_target = field(int)
    message3 = field(Message)

    item_type = field(ItemType)

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.ENEMY_SPAWN

    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        raise NotImplementedError

    @classmethod
    def create(
        cls,
        node_name: str = "",
        layer_state: typing.Sequence[bool | int] = (False,) * 16,
        entity_id: int = -1,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        enemy_type: EnemyType | None = None,
        enemy_fields: EnemyFields | None = None,
        linked_entity_id: int = 0,
        spawn_limit: int = 1,
        spawn_total: int = 1,
        spawn_count: int = 1,
        active: bool = True,
        always_active: bool = True,
        item_chance: int = 100,
        spawner_health: int = 0,
        cooldown_time: int = 0,
        initial_cooldown: int = 0,
        active_distance: float = 30.0,
        enemy_active_distance: float = 35.0,
        enemy_node_name: str = "",
        message1_target: int = -1,
        message1: Message = Message.NONE,
        message2_target: int = -1,
        message2: Message = Message.NONE,
        message3_target: int = -1,
        message3: Message = Message.NONE,
        item_type: ItemType = ItemType.NONE,
    ) -> typing.Self:
        if enemy_type is None:
            enemy_type = Hunter.cls_enemy_type()
        if enemy_fields is None:
            enemy_fields = Hunter.create()

        obj = super().create(
            node_name,
            layer_state,
            entity_id,
            position,
            up_vector,
            facing_vector,
        )
        obj.enemy_type = enemy_type
        obj.enemy_fields = enemy_fields
        obj.linked_entity_id = linked_entity_id
        obj.spawn_limit = spawn_limit
        obj.spawn_total = spawn_total
        obj.spawn_count = spawn_count
        obj.active = active
        obj.always_active = always_active
        obj.item_chance = item_chance
        obj.spawner_health = spawner_health
        obj.cooldown_time = cooldown_time
        obj.initial_cooldown = initial_cooldown
        obj.active_distance = active_distance
        obj.enemy_active_distance = enemy_active_distance
        obj.enemy_node_name = enemy_node_name
        obj.message1_target = message1_target
        obj.message1 = message1
        obj.message2_target = message2_target
        obj.message2 = message2
        obj.message3_target = message3_target
        obj.message3 = message3
        obj.item_type = item_type

        return obj
