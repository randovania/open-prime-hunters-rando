from construct import Construct, Int32sl, Int32ul, Struct

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, CollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields

Petrasyl234EntityData = Struct(
    "volume" / CollisionVolume,
    "_unused" / Int32ul[4],
    "position" / Vector3Fx,
    "weave_offset" / Int32ul,
    "field5" / Int32sl,
)


class Petrasyl234(EnemyFields, default_field_location="raw"):
    @classmethod
    def type_construct(cls) -> Construct:
        return Petrasyl234EntityData

    volume = field(BaseVolumeType)

    position = field(Vec3)

    weave_offset = field(int)

    field5 = field(int)
