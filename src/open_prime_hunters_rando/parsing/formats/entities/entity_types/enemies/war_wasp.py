import typing

from construct import Byte, Construct, Int32ul, Padded, Struct

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.common_types.volume import (
    BaseVolumeType,
    BoxVolumeType,
    CollisionVolume,
    SphereVolumeType,
)
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields, EnemyType

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

    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.WAR_WASP

    @classmethod
    def create(
        cls,
        volume1: BaseVolumeType | None = None,
        volume2: BaseVolumeType | None = None,
        volume3: BaseVolumeType | None = None,
        movement_vectors: list[Vec3 | tuple[float, float, float]] = [(0.0, 0.0, 0.0)] * 16,
        position_count: int = 0,
        movement_type: int = 0,
    ) -> typing.Self:
        if volume1 is None:
            volume1 = SphereVolumeType.create()
        if volume2 is None:
            volume2 = SphereVolumeType.create()
        if volume3 is None:
            volume3 = BoxVolumeType.create()

        war_wasp = super().create()

        war_wasp.volume1 = volume1
        war_wasp.volume2 = volume2
        war_wasp.volume3 = volume3
        war_wasp.movement_vectors = [Vec3(*mv) for mv in movement_vectors]
        war_wasp.position_count = position_count
        war_wasp.movement_type = movement_type

        return war_wasp


class BarbedWarWasp(WarWasp, default_field_location="raw"):
    @classmethod
    def type_construct(cls) -> Construct:
        return BarbedWarWaspEntityData

    enemy_subtype = field(int)
    enemy_version = field(int)

    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.BARBED_WAR_WASP

    @classmethod
    def create(
        cls,
        volume1: BaseVolumeType | None = None,
        volume2: BaseVolumeType | None = None,
        volume3: BaseVolumeType | None = None,
        movement_vectors: list[Vec3 | tuple[float, float, float]] = [(0.0, 0.0, 0.0)] * 16,
        position_count: int = 0,
        movement_type: int = 0,
        enemy_subtype: int = 0,
        enemy_version: int = 0,
    ) -> typing.Self:
        barbed_war_wasp = super().create(
            volume1,
            volume2,
            volume3,
            movement_vectors,
            position_count,
            movement_type,
        )

        barbed_war_wasp.enemy_subtype = enemy_subtype
        barbed_war_wasp.enemy_version = enemy_version

        return barbed_war_wasp
