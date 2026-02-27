from construct import Construct, Struct

from open_prime_hunters_rando.entities.entity import Entity
from open_prime_hunters_rando.entities.entity_file import EntityDataHeader
from open_prime_hunters_rando.entities.entity_types.volume_type import RawCollisionVolume, VolumeTypeCommon

DefenseNodeEntityData = Struct(
    "header" / EntityDataHeader,
    "volume" / RawCollisionVolume,
)


class DefenseNode(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return DefenseNodeEntityData

    def get_volume(self) -> VolumeTypeCommon:
        return VolumeTypeCommon(self._raw.data.volume)
