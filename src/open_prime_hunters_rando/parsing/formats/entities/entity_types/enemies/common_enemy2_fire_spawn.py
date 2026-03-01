from construct import Construct, Int32ul, Struct

from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, RawCollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemy_spawn import BaseEnemySpawn

CommonEnemy2FireSpawnEntityData = Struct(
    "enemy_subtype" / Int32ul,
    "enemy_version" / Int32ul,
    "volume1" / RawCollisionVolume,
    "volume2" / RawCollisionVolume,
    "volume3" / RawCollisionVolume,
    "volume4" / RawCollisionVolume,
)


class CommonEnemy2FireSpawnSpawnField(BaseEnemySpawn):
    @classmethod
    def type_construct(cls) -> Construct:
        return CommonEnemy2FireSpawnEntityData

    enemy_subtype = field(int)
    enemy_version = field(int)

    volume1 = field(BaseVolumeType)
    volume2 = field(BaseVolumeType)
    volume3 = field(BaseVolumeType)
    volume4 = field(BaseVolumeType)
