import typing

from construct import Byte, Construct, Flag, Int16sl, Int16ul, Int32sl, Int32ul, Struct
from construct.lib import Container

from open_prime_hunters_rando.common import Vec3
from open_prime_hunters_rando.entities.entity import Entity
from open_prime_hunters_rando.entities.entity_file import EntityDataHeader, ItemTypeConstruct, MessageConstruct
from open_prime_hunters_rando.entities.enum import EntityType, ItemType, Message

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


class ItemSpawn(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return ItemSpawnEntityData

    @property
    def parent_id(self) -> int:
        return self._raw.data.parent_id

    @parent_id.setter
    def parent_id(self, value: int) -> None:
        self._raw.data.parent_id = value

    @property
    def item_type(self) -> ItemType:
        return self._raw.data.item_type

    @item_type.setter
    def item_type(self, value: ItemType) -> None:
        self._raw.data.item_type = value

    @property
    def enabled(self) -> bool:
        return self._raw.data.enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._raw.data.enabled = value

    @property
    def has_base(self) -> bool:
        return self._raw.data.has_base

    @has_base.setter
    def has_base(self, value: bool) -> None:
        self._raw.data.has_base = value

    @property
    def always_active(self) -> bool:
        return self._raw.data.always_active

    @always_active.setter
    def always_active(self, value: bool) -> None:
        self._raw.data.always_active = value

    @property
    def max_spawn_count(self) -> int:
        return self._raw.data.max_spawn_count

    @max_spawn_count.setter
    def max_spawn_count(self, value: int) -> None:
        self._raw.data.max_spawn_count = value

    @property
    def spawn_interval(self) -> int:
        return self._raw.data.spawn_interval

    @spawn_interval.setter
    def spawn_interval(self, value: int) -> None:
        self._raw.data.spawn_interval = value

    @property
    def spawn_delay(self) -> int:
        return self._raw.data.spawn_delay

    @spawn_delay.setter
    def spawn_delay(self, value: int) -> None:
        self._raw.data.spawn_delay = value

    @property
    def notify_entity_id(self) -> int:
        return self._raw.data.notify_entity_id

    @notify_entity_id.setter
    def notify_entity_id(self, value: int) -> None:
        self._raw.data.notify_entity_id = value

    @property
    def collected_message(self) -> Message:
        return self._raw.data.collected_message

    @collected_message.setter
    def collected_message(self, value: Message) -> None:
        self._raw.data.collected_message = value

    @property
    def collected_message_param1(self) -> int:
        return self._raw.data.collected_message_param1

    @collected_message_param1.setter
    def collected_message_param1(self, value: int) -> None:
        self._raw.data.collected_message_param1 = value

    @property
    def collected_message_param2(self) -> int:
        return self._raw.data.collected_message_param2

    @collected_message_param2.setter
    def collected_message_param2(self, value: int) -> None:
        self._raw.data.collected_message_param2 = value

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.ITEM_SPAWN

    @classmethod
    def create(
        cls,
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
        data = Container(
            {
                "header": cls.create_header(position, up_vector, facing_vector),
                "parent_id": parent_id,
                "item_type": item_type,
                "enabled": enabled,
                "has_base": has_base,
                "always_active": always_active,
                "_padding": 0,
                "max_spawn_count": max_spawn_count,
                "spawn_interval": spawn_interval,
                "spawn_delay": spawn_delay,
                "notify_entity_id": notify_entity_id,
                "collected_message": collected_message,
                "collected_message_param1": collected_message_param1,
                "collected_message_param2": collected_message_param2,
            }
        )
        return cls(Container({"data": data}))
