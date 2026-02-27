from collections.abc import Collection
from typing import Any, Self

from construct import Construct, Container, ListContainer

from open_prime_hunters_rando.common import Vec3
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType


class Entity:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @classmethod
    def create_from_template(
        cls, data: Container, node_name: str = "rmMain", active_layers: Collection[int] = tuple(range(16))
    ) -> Self:
        layer_state = [False] * 16
        for layer in active_layers:
            layer_state[layer] = False

        return cls(
            Container(
                {
                    "node_name": node_name,
                    "layer_state": ListContainer(layer_state),
                    "data": data,
                }
            )
        )

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        raise NotImplementedError

    @classmethod
    def create_header(
        cls,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
    ) -> Container:
        return Container(
            {
                "entity_type": cls.cls_entity_type(),
                "position": Container(position),
                "up_vector": Container(up_vector),
                "facing_vector": Container(facing_vector),
            }
        )

    @classmethod
    def create(
        cls,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
    ) -> Self:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<Entity type={self.entity_type} id={self.entity_id}>"

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, Entity):
            return False
        if value.node_name != self.node_name:
            return False
        for i in range(16):
            if value.layer_state(i) != self.layer_state(i):
                return False

        def check_container(container: dict, other: dict) -> bool:
            for k in container.keys() | other.keys():
                if k.startswith("_"):
                    continue
                if isinstance(container[k], dict):
                    if not isinstance(other[k], dict):
                        return False
                    if not check_container(container[k], other[k]):
                        return False
                else:
                    if container[k] != other[k]:
                        return False
            return True

        return check_container(self._raw, value._raw)

    @property
    def node_name(self) -> str:
        return self._raw.node_name

    @node_name.setter
    def node_name(self, value: str) -> None:
        self._raw.node_name = value

    @property
    def active_layers(self) -> tuple[int, ...]:
        return tuple(i for i in range(16) if self.layer_state(i))

    def layer_state(self, layer: int) -> bool:
        return self._raw.layer_state[layer]

    def set_layer_state(self, layer: int, state: bool) -> None:
        self._raw.layer_state[layer] = state

    @property
    def entity_type(self) -> EntityType:
        return self.header.entity_type

    @entity_type.setter
    def entity_type(self, value: EntityType) -> None:
        self.header.entity_type = value

    @property
    def entity_id(self) -> int:
        return self.header.entity_id

    @entity_id.setter
    def entity_id(self, value: int) -> None:
        self.header.entity_id = value

    @property
    def data(self) -> Container:
        return self._raw.data

    @data.setter
    def data(self, value: Container) -> None:
        self._raw.data = value

    @property
    def header(self) -> Container:
        return self.data.header

    @header.setter
    def header(self, value: Container) -> None:
        self.data.header = value

    @property
    def position(self) -> Vec3:
        return self.header.position

    @position.setter
    def position(self, value: Vec3) -> None:
        self.header.position = value

    @property
    def up_vector(self) -> Vec3:
        return self.header.up_vector

    @up_vector.setter
    def up_vector(self, value: Vec3) -> None:
        self.header.up_vector = value

    @property
    def facing_vector(self) -> Vec3:
        return self.header.facing_vector

    @facing_vector.setter
    def facing_vector(self, value: Vec3) -> None:
        self.header.facing_vector = value

    @classmethod
    def type_construct(cls) -> Construct:
        raise NotImplementedError

    @property
    def size(self) -> int:
        return self.type_construct().sizeof()
