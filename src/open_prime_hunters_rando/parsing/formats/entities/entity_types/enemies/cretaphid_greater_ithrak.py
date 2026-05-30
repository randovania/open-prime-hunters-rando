import typing

from construct import Construct, Int32ul, Struct

from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, BoxVolumeType, CollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields, EnemyType

CretaphidGreaterIthrakEntityData = Struct(
    "enemy_subtype" / Int32ul,
    "volume1" / CollisionVolume,
    "volume2" / CollisionVolume,
    "volume3" / CollisionVolume,
    "volume4" / CollisionVolume,
)


class CretaphidGreaterIthrak(EnemyFields, default_field_location="raw"):
    @classmethod
    def type_construct(cls) -> Construct:
        return CretaphidGreaterIthrakEntityData

    enemy_subtype = field(int)

    volume1 = field(BaseVolumeType)
    volume2 = field(BaseVolumeType)
    volume3 = field(BaseVolumeType)
    volume4 = field(BaseVolumeType)

    @classmethod
    def create(
        cls,
        enemy_subtype: int = 0,
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

        enemy.enemy_subtype = enemy_subtype
        enemy.volume1 = volume1
        enemy.volume2 = volume2
        enemy.volume3 = volume3
        enemy.volume4 = volume4

        return enemy


class Creatphid(CretaphidGreaterIthrak):
    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.CRETAPHID


class GreaterIthrak(CretaphidGreaterIthrak):
    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.GREATER_ITHRAK
