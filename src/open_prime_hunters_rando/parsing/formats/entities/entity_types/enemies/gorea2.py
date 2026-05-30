import typing

from construct import Construct, Int32ul, Struct

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields, EnemyType

Gorea2EntityData = Struct(
    "field1" / Vector3Fx,
    "field2" / Int32ul,
    "field3" / Int32ul,
)


class Gorea2(EnemyFields, default_field_location="raw"):
    @classmethod
    def type_construct(cls) -> Construct:
        return Gorea2EntityData

    field1 = field(Vec3)
    field2 = field(int)
    field3 = field(int)

    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.GOREA2

    @classmethod
    def create(
        cls,
        field1: Vec3 | tuple[float, float, float] = (-1.396240234375, 48.457763671875, 3.910400390625),
        field2: int = 16384,
        field3: int = 163840,
    ) -> typing.Self:
        gorea2 = super().create()

        gorea2.field1 = Vec3(*field1)
        gorea2.field2 = field2
        gorea2.field3 = field3

        return gorea2
