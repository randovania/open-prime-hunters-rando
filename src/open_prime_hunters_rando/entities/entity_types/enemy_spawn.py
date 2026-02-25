from construct import Container

from open_prime_hunters_rando.entities.entity import Entity
from open_prime_hunters_rando.entities.enum import EnemyType, ItemType, Message


class EnemySpawn(Entity):
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
