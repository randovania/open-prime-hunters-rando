from construct import Byte, Construct, Struct

from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field

OctolithFlagEntityData = Struct(
    "team_id" / Byte,
)


class OctolithFlag(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return OctolithFlagEntityData

    team_id = field(int)
