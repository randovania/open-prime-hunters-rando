from open_prime_hunters_rando.entities.entity_type import Entity
from open_prime_hunters_rando.entities.enum import VolumeType


class MorphCamera(Entity):
    def get_volume(self) -> VolumeType:
        return VolumeType(self._raw.data.volume)
