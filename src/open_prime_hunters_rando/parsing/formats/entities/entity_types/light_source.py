from construct import Construct, Flag, Struct

from open_prime_hunters_rando.common import Rgb01, Vec3
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_file import EntityDataHeader, Vector3Fx
from open_prime_hunters_rando.parsing.formats.entities.entity_types.volume_type import RawCollisionVolume, VolumeTypeCommon

ColorRgb = Struct(
    "red" / Rgb01,
    "green" / Rgb01,
    "blue" / Rgb01,
)

LightSourceEntityData = Struct(
    "header" / EntityDataHeader,
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

    def get_volume(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume)

    @property
    def light1_enabled(self) -> bool:
        return self._raw.data.light1_enabled

    @light1_enabled.setter
    def light1_enabled(self, value: bool) -> None:
        self._raw.data.light1_enabled = value

    @property
    def light1_color(self) -> Vec3:
        return self._raw.data.light1_color

    @light1_color.setter
    def light1_color(self, value: Vec3) -> None:
        self._raw.data.light1_color = value

    @property
    def light1_vector(self) -> Vec3:
        return self._raw.data.light1_vector

    @light1_vector.setter
    def light1_vector(self, value: Vec3) -> None:
        self._raw.data.light1_vector = value

    @property
    def light2_enabled(self) -> bool:
        return self._raw.data.light2_enabled

    @light2_enabled.setter
    def light2_enabled(self, value: bool) -> None:
        self._raw.data.light2_enabled = value

    @property
    def light2_color(self) -> Vec3:
        return self._raw.data.light2_color

    @light2_color.setter
    def light2_color(self, value: Vec3) -> None:
        self._raw.data.light2_color = value

    @property
    def light2_vector(self) -> Vec3:
        return self._raw.data.light2_vector

    @light2_vector.setter
    def light2_vector(self, value: Vec3) -> None:
        self._raw.data.light2_vector = value
