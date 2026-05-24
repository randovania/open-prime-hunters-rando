import typing

from construct import Construct, Container, Flag, Struct

from open_prime_hunters_rando.parsing.common_types import Rgb01
from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, BoxVolumeType, CollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType

ColorRgb = Struct(
    "red" / Rgb01,
    "green" / Rgb01,
    "blue" / Rgb01,
)

LightSourceEntityData = Struct(
    "volume" / CollisionVolume,
    "light1_enabled" / Flag,
    "light1_color" / ColorRgb,
    "light1_vector" / Vector3Fx,
    "light2_enabled" / Flag,
    "light2_color" / ColorRgb,
    "light2_vector" / Vector3Fx,
)


class LightSource(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return LightSourceEntityData

    volume = field(BaseVolumeType)

    light1_enabled = field(bool)
    light1_color = field(Container)
    light1_vector = field(Vec3)

    light2_enabled = field(bool)
    light2_color = field(Container)
    light2_vector = field(Vec3)

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.LIGHT_SOURCE

    @classmethod
    def create(
        cls,
        node_name: str = "",
        layer_state: typing.Sequence[bool | int] = (False,) * 16,
        entity_id: int = -1,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 1.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 1.0),
        volume: BaseVolumeType | None = None,
        light1_enabled: bool = True,
        light1_color: Container = Container(red=0.0, green=0.0, blue=0.0),
        light1_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        light2_enabled: bool = True,
        light2_color: Container = Container(red=0.0, green=0.0, blue=0.0),
        light2_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
    ) -> typing.Self:
        if volume is None:
            volume = BoxVolumeType.create()

        obj = super().create(
            node_name,
            layer_state,
            entity_id,
            position,
            up_vector,
            facing_vector,
        )
        obj.volume = volume
        obj.light1_enabled = light1_enabled
        obj.light1_color = light1_color
        obj.light1_vector = Vec3(*light1_vector)
        obj.light2_enabled = light2_enabled
        obj.light2_color = light2_color
        obj.light2_vector = Vec3(*light2_vector)

        return obj
