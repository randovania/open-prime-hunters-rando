import typing

from construct import Construct, Int32ul, Struct

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, CollisionVolume, SphereVolumeType
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields, EnemyType

TemroidPetrasyllEntityData = Struct(
    "volume" / CollisionVolume,
    "field2" / Int32ul,  # Unused
    "field3" / Int32ul,  # Unused
    "field4" / Int32ul,  # Unused
    "field5" / Int32ul,  # Unused
    "field6" / Int32ul,  # Unused
    "field7" / Int32ul,  # Unused
    "field8" / Int32ul,  # Unused
    "facing" / Vector3Fx,
    "position" / Vector3Fx,
    "idle_range" / Vector3Fx,
)


class TemroidPetrasyl1(EnemyFields, default_field_location="raw"):
    @classmethod
    def type_construct(cls) -> Construct:
        return TemroidPetrasyllEntityData

    volume = field(BaseVolumeType)

    field2 = field(int)
    field3 = field(int)
    field4 = field(int)
    field5 = field(int)
    field6 = field(int)
    field7 = field(int)
    field8 = field(int)

    facing = field(Vec3)
    position = field(Vec3)

    idle_range = field(Vec3)

    @classmethod
    def create(
        cls,
        volume: BaseVolumeType | None = None,
        field2: int = 0,
        field3: int = 0,
        field4: int = 0,
        field5: int = 0,
        field6: int = 0,
        field7: int = 0,
        field8: int = 0,
        facing: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        idle_range: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
    ) -> typing.Self:
        if volume is None:
            volume = SphereVolumeType.create()
        temroid_petrasyl1 = super().create()

        temroid_petrasyl1.volume = volume
        temroid_petrasyl1.field2 = field2
        temroid_petrasyl1.field3 = field3
        temroid_petrasyl1.field4 = field4
        temroid_petrasyl1.field5 = field5
        temroid_petrasyl1.field6 = field6
        temroid_petrasyl1.field7 = field7
        temroid_petrasyl1.field8 = field8
        temroid_petrasyl1.facing = Vec3(*facing)
        temroid_petrasyl1.position = Vec3(*position)
        temroid_petrasyl1.idle_range = Vec3(*idle_range)

        return temroid_petrasyl1


class Temroid(TemroidPetrasyl1):
    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.TEMROID


class Petrasyl1(TemroidPetrasyl1):
    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.PETRASYL1
