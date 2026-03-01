from construct import Construct, Int32ul, Struct

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields

Gorea2EntityData = Struct(
    "field1" / Vector3Fx,
    "field2" / Int32ul,
    "field3" / Int32ul,
)


class Gorea2(EnemyFields):
    @classmethod
    def type_construct(cls) -> Construct:
        return Gorea2EntityData

    field1 = field(Vec3)
    field2 = field(int)
    field3 = field(int)
