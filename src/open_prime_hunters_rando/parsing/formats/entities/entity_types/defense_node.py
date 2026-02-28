from construct import Construct, Struct

from open_prime_hunters_rando.parsing.common_types.volume import RawCollisionVolume, VolumeTypeCommon
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_file import EntityDataHeader

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
