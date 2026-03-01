from construct import Construct, Int32ul, Struct

from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, RawCollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field

FlagBaseEntityData = Struct(
    "team_id" / Int32ul,
    "volume" / RawCollisionVolume,
)


class FlagBase(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return FlagBaseEntityData

    team_id = field(int)

    volume = field(BaseVolumeType)
