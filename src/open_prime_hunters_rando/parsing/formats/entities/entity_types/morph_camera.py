from construct import Construct, Struct

from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, CollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field

MorphCameraEntityData = Struct(
    "volume" / CollisionVolume,
)


class MorphCamera(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return MorphCameraEntityData

    volume = field(BaseVolumeType)
