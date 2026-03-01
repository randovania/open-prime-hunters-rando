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
from open_prime_hunters_rando.parsing.construct_extensions import EnumAdapter
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies import enemy_type_to_class
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields, EnemyType
from open_prime_hunters_rando.parsing.formats.entities.enum import ItemType, Message

EnemyTypeConstruct = EnumAdapter(EnemyType, Byte)


EnemySpawnEntityData = Struct(
    "enemy_type" / Padded(4, EnemyTypeConstruct),
    "fields_raw" / Padded(400, Switch(construct.this.enemy_type, enemy_type_to_class)),
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
    "node_name" / DecodedString,
    "entity_id1" / Padded(4, Int16sl),
    "message1" / MessageConstruct,
    "entity_id2" / Padded(4, Int16sl),
    "message2" / MessageConstruct,
    "entity_id3" / Padded(4, Int16sl),
    "message3" / MessageConstruct,
    "item_type" / ItemTypeConstruct,
)


class EnemySpawn(Entity):
    def __init__(self, raw: Container) -> None:
        super().__init__(raw)
        self.fields = enemy_type_to_class[self.enemy_type](self.fields_raw)

    @classmethod
    def type_construct(cls) -> Construct:
        return EnemySpawnEntityData

    enemy_type = field(EnemyType)

    fields_raw = field(Container)
    fields: EnemyFields

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

    node_name = field(str)

    entity_id1 = field(int)
    message1 = field(Message)

    entity_id2 = field(int)
    message2 = field(Message)

    entity_id3 = field(int)
    message3 = field(Message)

    item_type = field(ItemType)
