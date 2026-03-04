from construct import Byte, Construct, Struct

from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field

PlayerSpawnEntityData = Struct(
    "availability" / Byte,
    "active" / Byte,
    "team_index" / Byte,
)


class PlayerSpawn(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return PlayerSpawnEntityData

    availability = field(int)

    active = field(int)

    team_index = field(int)
