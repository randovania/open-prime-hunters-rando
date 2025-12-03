from construct import Container

from open_prime_hunters_rando.common import Vec3
from open_prime_hunters_rando.entities.enum import VolumeType


class LightSource:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def get_volume(self) -> VolumeType:
        return VolumeType(self._raw.volume)

    @property
    def light1_enabled(self) -> bool:
        return self._raw.light1_enabled

    @light1_enabled.setter
    def light1_enabled(self, value: bool) -> None:
        self._raw.light1_enabled = value

    @property
    def light1_color(self) -> Vec3:
        return self._raw.light1_color

    @light1_color.setter
    def light1_color(self, value: Vec3) -> None:
        self._raw.light1_color = value

    @property
    def light1_vector(self) -> Vec3:
        return self._raw.light1_vector

    @light1_vector.setter
    def light1_vector(self, value: Vec3) -> None:
        self._raw.light1_vector = value

    @property
    def light2_enabled(self) -> bool:
        return self._raw.light2_enabled

    @light2_enabled.setter
    def light2_enabled(self, value: bool) -> None:
        self._raw.light2_enabled = value

    @property
    def light2_color(self) -> Vec3:
        return self._raw.light2_color

    @light2_color.setter
    def light2_color(self, value: Vec3) -> None:
        self._raw.light2_color = value

    @property
    def light2_vector(self) -> Vec3:
        return self._raw.light2_vector

    @light2_vector.setter
    def light2_vector(self, value: Vec3) -> None:
        self._raw.light2_vector = value
