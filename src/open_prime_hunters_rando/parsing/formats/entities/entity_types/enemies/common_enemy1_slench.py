import typing

from construct import Construct, Struct

from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, BoxVolumeType, CollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields, EnemyType

CommonEnemy1SlenchEntityData = Struct(
    "volume1" / CollisionVolume,
    "volume2" / CollisionVolume,
    "volume3" / CollisionVolume,
    "volume4" / CollisionVolume,
)


class CommonEnemy1Slench(EnemyFields, default_field_location="raw"):
    @classmethod
    def type_construct(cls) -> Construct:
        return CommonEnemy1SlenchEntityData

    volume1 = field(BaseVolumeType)
    volume2 = field(BaseVolumeType)
    volume3 = field(BaseVolumeType)
    volume4 = field(BaseVolumeType)

    @classmethod
    def create(
        cls,
        volume1: BaseVolumeType | None = None,
        volume2: BaseVolumeType | None = None,
        volume3: BaseVolumeType | None = None,
        volume4: BaseVolumeType | None = None,
    ) -> typing.Self:
        if volume1 is None:
            volume1 = BoxVolumeType.create()
        if volume2 is None:
            volume2 = BoxVolumeType.create()
        if volume3 is None:
            volume3 = BoxVolumeType.create()
        if volume4 is None:
            volume4 = BoxVolumeType.create()

        enemy = super().create()

        enemy.volume1 = volume1
        enemy.volume2 = volume2
        enemy.volume3 = volume3
        enemy.volume4 = volume4

        return enemy


class Zoomer(CommonEnemy1Slench):
    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.ZOOMER


class Geemer(CommonEnemy1Slench):
    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.GEEMER


class Blastcap(CommonEnemy1Slench):
    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.BLASTCAP


class Quadtroid(CommonEnemy1Slench):
    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.QUADTROID


class CrashPillar(CommonEnemy1Slench):
    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.CRASH_PILLAR


class Slench(CommonEnemy1Slench):
    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.SLENCH


class LesserIthrak(CommonEnemy1Slench):
    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.LESSER_ITHRAK


class Trocra(CommonEnemy1Slench):
    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.TROCRA


class Voldrum2(CommonEnemy1Slench):
    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.VOLDRUM2
