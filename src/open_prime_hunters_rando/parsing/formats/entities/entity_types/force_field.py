import typing

from construct import Construct, Flag, Struct

from open_prime_hunters_rando.parsing.common_types import FixedPoint, WeaponTypeConstruct
from open_prime_hunters_rando.parsing.common_types.vectors import Vec3
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType, WeaponType

ForceFieldEntityData = Struct(
    "force_field_type" / WeaponTypeConstruct,
    "width" / FixedPoint,
    "height" / FixedPoint,
    "active" / Flag,
)


class ForceField(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return ForceFieldEntityData

    force_field_type = field(WeaponType)

    width = field(float)
    height = field(float)

    active = field(bool)

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.FORCE_FIELD

    @classmethod
    def create(
        cls,
        node_name: str = "",
        layer_state: typing.Sequence[bool | int] = (False,) * 16,
        entity_id: int = -1,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 1.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 1.0),
        force_field_type: WeaponType = WeaponType.LOCKED,
        width: float = 0.0,
        height: float = 0.0,
        active: bool = False,
    ) -> typing.Self:
        obj = super().create(
            node_name,
            layer_state,
            entity_id,
            position,
            up_vector,
            facing_vector,
        )
        obj.force_field_type = force_field_type
        obj.width = width
        obj.height = height
        obj.active = active

        return obj
