import typing

from construct import Construct, Struct

from open_prime_hunters_rando.parsing.common_types import FixedPoint
from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields, EnemyType

Gorea1EntityData = Struct(
    "sphere1_position" / Vector3Fx,
    "sphere1_radius" / FixedPoint,
    "sphere2_position" / Vector3Fx,
    "sphere2_radius" / FixedPoint,
)


class Gorea1(EnemyFields, default_field_location="raw"):
    @classmethod
    def type_construct(cls) -> Construct:
        return Gorea1EntityData

    sphere1_position = field(Vec3)
    sphere1_radius = field(float)

    sphere2_position = field(Vec3)
    sphere2_radius = field(float)

    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.GOREA1_A

    @classmethod
    def create(
        cls,
        sphere1_position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        sphere1_radius: float = 17.5,
        sphere2_position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        sphere2_radius: float = 17.5,
    ) -> typing.Self:
        gorea1 = super().create()

        gorea1.sphere1_position = Vec3(*sphere1_position)
        gorea1.sphere1_radius = sphere1_radius
        gorea1.sphere2_position = Vec3(*sphere2_position)
        gorea1.sphere2_radius = sphere2_radius

        return gorea1
