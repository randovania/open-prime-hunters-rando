from construct import Byte, Construct, Int32ul, Padded, Struct

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, CollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields

WarWaspEntityData = Struct(
    "volume1" / CollisionVolume,
    "volume2" / CollisionVolume,
    "volume3" / CollisionVolume,
    "movement_vectors" / Vector3Fx[16],
    "position_count" / Padded(4, Byte),
    "movement_type" / Int32ul,
)

BarbedWarWaspEntityData = Struct(
    "enemy_subtype" / Int32ul,
    "enemy_version" / Int32ul,
    "data" / WarWaspEntityData,
)


class WarWasp(EnemyFields, default_field_location="raw"):
    @classmethod
    def type_construct(cls) -> Construct:
        return WarWaspEntityData

    volume1 = field(BaseVolumeType)
    volume2 = field(BaseVolumeType)
    volume3 = field(BaseVolumeType)

    movement_vectors = field(list[Vec3])

    position_count = field(int)

    movement_type = field(int)


class BarbedWarWasp(WarWasp, default_field_location="raw"):
    @classmethod
    def type_construct(cls) -> Construct:
        return BarbedWarWaspEntityData

    enemy_subtype = field(int)
    enemy_version = field(int)
