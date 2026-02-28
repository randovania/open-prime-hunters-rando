from construct import Construct, Flag, Struct

from open_prime_hunters_rando.common import FixedPoint
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_file import PaletteIdConstruct
from open_prime_hunters_rando.parsing.formats.entities.enum import PaletteId

ForceFieldEntityData = Struct(
    "force_field_type" / PaletteIdConstruct,
    "width" / FixedPoint,
    "height" / FixedPoint,
    "active" / Flag,
)


class ForceField(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return ForceFieldEntityData

    force_field_type = field(PaletteId)

    width = field(float)
    height = field(float)

    active = field(bool)
