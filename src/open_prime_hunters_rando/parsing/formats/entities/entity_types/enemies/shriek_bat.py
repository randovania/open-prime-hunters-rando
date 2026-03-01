from construct import Construct, Struct

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, CollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields

ShriekBatEntityData = Struct(
    "volume1" / CollisionVolume,
    "path_vector" / Vector3Fx,
    "volume2" / CollisionVolume,
    "volume3" / CollisionVolume,
)


class ShriekBat(EnemyFields):
    @classmethod
    def type_construct(cls) -> Construct:
        return ShriekBatEntityData

    volume1 = field(BaseVolumeType)

    path_vector = field(Vec3)

    volume2 = field(BaseVolumeType)
    volume3 = field(BaseVolumeType)
