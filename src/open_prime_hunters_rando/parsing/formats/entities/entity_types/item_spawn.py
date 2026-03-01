import typing

from construct import Construct, Flag, Int16sl, Int16ul, Int32sl, Int32ul, Padded, Struct

from open_prime_hunters_rando.parsing.common_types import ItemTypeConstruct, MessageConstruct
from open_prime_hunters_rando.parsing.common_types.vectors import Vec3
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType, ItemType, Message

ItemSpawnEntityData = Struct(
    "parent_id" / Int32sl,
    "item_type" / ItemTypeConstruct,
    "enabled" / Flag,
    "has_base" / Flag,
    "always_active" / Padded(2, Flag),
    "max_spawn_count" / Int16ul,
    "spawn_interval" / Int16ul,
    "spawn_delay" / Int16ul,
    "notify_entity_id" / Int16sl,
    "collected_message" / MessageConstruct,
    "collected_message_param1" / Int32ul,
    "collected_message_param2" / Int32ul,
)


class ItemSpawn(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return ItemSpawnEntityData

    parent_id = field(int)
    item_type = field(int)

    enabled = field(bool)
    has_base = field(bool)
    always_active = field(bool)

    max_spawn_count = field(int)
    spawn_interval = field(int)
    spawn_delay = field(int)

    notify_entity_id = field(int)
    collected_message = field(Message)
    collected_message_param1 = field(int)
    collected_message_param2 = field(int)

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.ITEM_SPAWN

    @classmethod
    def create(
        cls,
        node_name: str = "",
        layer_state: typing.Sequence[bool] = (False,) * 16,
        entity_id: int = -1,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        parent_id: int = 65535,
        item_type: ItemType = ItemType.HEALTH_SMALL,
        enabled: bool = True,
        has_base: bool = False,
        always_active: bool = False,
        max_spawn_count: int = 1,
        spawn_interval: int = 0,
        spawn_delay: int = 0,
        notify_entity_id: int = 0,
        collected_message: Message = Message.NONE,
        collected_message_param1: int = 0,
        collected_message_param2: int = 0,
    ) -> typing.Self:
        obj = super().create(
            node_name,
            layer_state,
            entity_id,
            position,
            up_vector,
            facing_vector,
        )
        obj.parent_id = parent_id
        obj.item_type = item_type
        obj.enabled = enabled
        obj.has_base = has_base
        obj.always_active = always_active
        obj.max_spawn_count = max_spawn_count
        obj.spawn_interval = spawn_interval
        obj.spawn_delay = spawn_delay
        obj.notify_entity_id = notify_entity_id
        obj.collected_message = collected_message
        obj.collected_message_param1 = collected_message_param1
        obj.collected_message_param2 = collected_message_param2

        return obj
