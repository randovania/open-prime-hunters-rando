import typing

from construct import Construct, Int32sl, Int32ul, Struct

from open_prime_hunters_rando.parsing.common_types.volume import (
    BaseVolumeType,
    BoxVolumeType,
    CollisionVolume,
    SphereVolumeType,
)
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields, EnemyType

SlenchTurretEntityData = Struct(
    "enemy_subtype" / Int32ul,
    "enemy_version" / Int32ul,
    "volume1" / CollisionVolume,
    "volume2" / CollisionVolume,
    "index" / Int32sl,
)


class SlenchTurret(EnemyFields, default_field_location="raw"):
    @classmethod
    def type_construct(cls) -> Construct:
        return SlenchTurretEntityData

    enemy_subtype = field(int)
    enemy_version = field(int)

    volume1 = field(BaseVolumeType)
    volume2 = field(BaseVolumeType)

    index = field(int)

    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.SLENCH_TURRET

    @classmethod
    def create(
        cls,
        enemy_subtype: int = 0,
        enemy_version: int = 0,
        volume1: BaseVolumeType | None = None,
        volume2: BaseVolumeType | None = None,
        index: int = 0,
    ) -> typing.Self:
        if volume1 is None:
            volume1 = BoxVolumeType.create()
        if volume2 is None:
            volume2 = SphereVolumeType.create()

        slench_turret = super().create()

        slench_turret.enemy_subtype = enemy_subtype
        slench_turret.enemy_version = enemy_version
        slench_turret.volume1 = volume1
        slench_turret.volume2 = volume2
        slench_turret.index = index

        return slench_turret
