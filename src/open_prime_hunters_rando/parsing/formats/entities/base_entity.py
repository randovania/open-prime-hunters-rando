from collections.abc import Collection, Sequence
from typing import ClassVar, Self

from construct import Construct, Container, ListContainer

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import EntityField, field
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType


class Entity:
    _fields: ClassVar[dict[str, EntityField]] = {}

    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def __init_subclass__(cls) -> None:
        # give each subclass a unique list
        cls._fields = dict(Entity._fields)

    node_name = field(str, "raw")

    layer_state = field(list[int], "raw")

    @property
    def active_layers(self) -> tuple[int, ...]:
        return tuple(i for i in range(16) if self.layer_state[i])

    entity_type = field(EntityType, "header")
    entity_id = field(int, "header")

    position = field(Vec3, "header")
    up_vector = field(Vec3, "header")
    facing_vector = field(Vec3, "header")

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
    def create(
        cls,
        node_name: str = "",
        layer_state: Sequence[bool] = (False,) * 16,
        entity_id: int = -1,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
    ) -> Self:
        default_data = Container(
            {
                "data": Container(
                    {
                        "header": Container(),
                        "fields": Container(),
                    }
                )
            }
        )
        entity = cls(default_data)

        entity.node_name = node_name
        entity.layer_state = ListContainer(layer_state)

        entity.entity_type = cls.cls_entity_type()
        entity.entity_id = entity_id

        entity.position = Vec3(*position)
        entity.up_vector = Vec3(*up_vector)
        entity.facing_vector = Vec3(*facing_vector)

        return entity

    def __repr__(self) -> str:
        return f"<Entity type={self.entity_type} id={self.entity_id}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False

        for field_name in self._fields.keys():
            if getattr(self, field_name, None) != getattr(other, field_name, None):
                return False

        return True

    @classmethod
    def type_construct(cls) -> Construct:
        raise NotImplementedError

    @property
    def size(self) -> int:
        return self.type_construct().sizeof()
