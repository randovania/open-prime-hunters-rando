from construct import Construct, Flag, Int16sl, Struct

from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field

PointModuleEntityData = Struct(
    "next_id" / Int16sl,
    "prev_id" / Int16sl,
    "active" / Flag,
)


class PointModule(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return PointModule

    next_id = field(int)
    prev_id = field(int)

    active = field(bool)
