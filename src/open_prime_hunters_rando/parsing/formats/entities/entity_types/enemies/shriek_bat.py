from construct import Construct, Struct

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, RawCollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemy_spawn import BaseEnemySpawn

ShriekBatEntityData = Struct(
    "volume1" / RawCollisionVolume,
    "path_vector" / Vector3Fx,
    "volume2" / RawCollisionVolume,
    "volume3" / RawCollisionVolume,
)


class ShriekBatSpawnField(BaseEnemySpawn):
    @classmethod
    def type_construct(cls) -> Construct:
        return ShriekBatEntityData

    volume1 = field(BaseVolumeType)

    path_vector = field(Vec3)

    volume2 = field(BaseVolumeType)
    volume3 = field(BaseVolumeType)
