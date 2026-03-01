from construct import Construct, Struct

from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, RawCollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field

DefenseNodeEntityData = Struct(
    "volume" / RawCollisionVolume,
)


class DefenseNode(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return DefenseNodeEntityData

    volume = field(BaseVolumeType)
