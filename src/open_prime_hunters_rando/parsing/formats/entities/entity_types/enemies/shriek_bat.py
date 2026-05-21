import typing

from construct import Construct, Struct

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.common_types.volume import (
    BaseVolumeType,
    BoxVolumeType,
    CollisionVolume,
    SphereVolumeType,
)
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields, EnemyType

ShriekBatEntityData = Struct(
    "volume1" / CollisionVolume,
    "path_vector" / Vector3Fx,
    "volume2" / CollisionVolume,
    "volume3" / CollisionVolume,
)


class ShriekBat(EnemyFields, default_field_location="raw"):
    @classmethod
    def type_construct(cls) -> Construct:
        return ShriekBatEntityData

    volume1 = field(BaseVolumeType)

    path_vector = field(Vec3)

    volume2 = field(BaseVolumeType)
    volume3 = field(BaseVolumeType)

    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.SHRIEKBAT

    @classmethod
    def create(
        cls,
        volume1: BaseVolumeType | None = None,
        path_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        volume2: BaseVolumeType | None = None,
        volume3: BaseVolumeType | None = None,
    ) -> typing.Self:
        if volume1 is None:
            volume1 = SphereVolumeType.create()
        if volume2 is None:
            volume2 = BoxVolumeType.create()
        if volume3 is None:
            volume3 = BoxVolumeType.create()

        shriekbat = super().create()

        shriekbat.volume1 = volume1
        shriekbat.path_vector = Vec3(*path_vector)
        shriekbat.volume2 = volume2
        shriekbat.volume3 = volume3

        return shriekbat
