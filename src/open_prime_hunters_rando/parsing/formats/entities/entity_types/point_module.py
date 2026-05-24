import typing

from construct import Construct, Flag, Int16sl, Struct

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType

PointModuleEntityData = Struct(
    "next_id" / Int16sl,
    "prev_id" / Int16sl,
    "active" / Flag,
)


class PointModule(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return PointModuleEntityData

    next_id = field(int)
    prev_id = field(int)

    active = field(bool)

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.POINT_MODULE

    @classmethod
    def create(
        cls,
        node_name: str = "",
        layer_state: typing.Sequence[bool | int] = (False,) * 16,
        entity_id: int = -1,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 1.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 1.0),
        next_id: int = 0,
        prev_id: int = 0,
        active: bool = True,
    ) -> typing.Self:
        obj = super().create(
            node_name,
            layer_state,
            entity_id,
            position,
            up_vector,
            facing_vector,
        )
        obj.next_id = next_id
        obj.prev_id = prev_id
        obj.active = active

        return obj
