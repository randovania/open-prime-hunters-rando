import typing

from construct import Byte, Construct, Struct

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType

OctolithFlagEntityData = Struct(
    "team_id" / Byte,
)


class OctolithFlag(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return OctolithFlagEntityData

    team_id = field(int)

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.OCTOLITH_FLAG

    @classmethod
    def create(
        cls,
        node_name: str = "",
        layer_state: typing.Sequence[bool] = (False,) * 16,
        entity_id: int = -1,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 1.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 1.0),
        team_id: int = 0,
    ) -> typing.Self:
        obj = super().create(
            node_name,
            layer_state,
            entity_id,
            position,
            up_vector,
            facing_vector,
        )
        obj.team_id = team_id

        return obj
