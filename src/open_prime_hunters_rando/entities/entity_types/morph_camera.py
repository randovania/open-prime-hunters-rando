from construct import Container

from open_prime_hunters_rando.entities.entity_type import VolumeType


class MorphCamera:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def get_volume(self) -> VolumeType:
        return VolumeType(self._raw.volume)
