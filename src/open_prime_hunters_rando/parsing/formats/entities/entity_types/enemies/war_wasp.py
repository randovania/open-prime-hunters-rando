from construct import Byte, Construct, Int32ul, Padded, Struct

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, RawCollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemy_spawn import BaseEnemySpawn

WarWaspEntityData = Struct(
    "volume1" / Padded(64, RawCollisionVolume),
    "volume2" / RawCollisionVolume,
    "volume3" / RawCollisionVolume,
    "movement_vectors" / Vector3Fx[16],
    "position_count" / Padded(4, Byte),
    "movement_type" / Padded(8, Int32ul),
)

BarbedWarWaspEntityData = Struct(
    "enemy_subtype" / Int32ul,
    "enemy_version" / Int32ul,
    "data" / WarWaspEntityData,
)


class WarWaspSpawnField(BaseEnemySpawn):
    @classmethod
    def type_construct(cls) -> Construct:
        return WarWaspEntityData

    volume1 = field(BaseVolumeType)
    volume2 = field(BaseVolumeType)
    volume3 = field(BaseVolumeType)

    movement_vectors = field([list[Vec3]])

    position_count = field(int)

    movement_type = field(int)


class BarbedWarWaspSpawnField(WarWaspSpawnField):
    @classmethod
    def type_construct(cls) -> Construct:
        return BarbedWarWaspEntityData

    enemy_subtype = field(int)
    enemy_version = field(int)
