from construct import Construct, Flag, Struct

from open_prime_hunters_rando.parsing.common_types import Rgb01
from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, RawCollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field

ColorRgb = Struct(
    "red" / Rgb01,
    "green" / Rgb01,
    "blue" / Rgb01,
)

LightSourceEntityData = Struct(
    "volume" / RawCollisionVolume,
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
    light1_color = field(Vec3)
    light1_vector = field(Vec3)

    light2_enabled = field(bool)
    light2_color = field(Vec3)
    light2_vector = field(Vec3)
