from construct import Container

from open_prime_hunters_rando.entities.entity_type import ItemType, Message


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
