import typing

from construct import Construct, Int32sl, Int32ul, Struct

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, CollisionVolume, SphereVolumeType
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields, EnemyType

Petrasyl234EntityData = Struct(
    "volume" / CollisionVolume,
    "field2" / Int32ul,  # Unused
    "field3" / Int32ul,  # Unused
    "field4" / Int32ul,  # Unused
    "field5" / Int32ul,  # Unused
    "position" / Vector3Fx,
    "weave_offset" / Int32ul,
    "field8" / Int32sl,
)


class Petrasyl234(EnemyFields, default_field_location="raw"):
    @classmethod
    def type_construct(cls) -> Construct:
        return Petrasyl234EntityData

    volume = field(BaseVolumeType)

    field2 = field(int)
    field3 = field(int)
    field4 = field(int)
    field5 = field(int)

    position = field(Vec3)

    weave_offset = field(int)

    field8 = field(int)

    @classmethod
    def create(
        cls,
        volume: BaseVolumeType | None = None,
        field2: int = 1,
        field3: int = 0,
        field4: int = 4096,
        field5: int = 0,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        weave_offset: int = 0,
        field8: int = 0,
    ) -> typing.Self:
        if volume is None:
            volume = SphereVolumeType.create()
        petrasyl234 = super().create()

        petrasyl234.volume = volume
        petrasyl234.field2 = field2
        petrasyl234.field3 = field3
        petrasyl234.field4 = field4
        petrasyl234.field5 = field5
        petrasyl234.position = Vec3(*position)
        petrasyl234.weave_offset = weave_offset
        petrasyl234.field8 = field8

        return petrasyl234


class Petrasyl2(Petrasyl234):
    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.PETRASYL2


class Petrasyl3(Petrasyl234):
    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.PETRASYL3


class Petrasyl4(Petrasyl234):
    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.PETRASYL4
