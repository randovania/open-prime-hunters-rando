from construct import Construct, Flag, Struct

from open_prime_hunters_rando.common import FixedPoint
from open_prime_hunters_rando.entities.entity import Entity
from open_prime_hunters_rando.entities.entity_file import EntityDataHeader, PaletteIdConstruct
from open_prime_hunters_rando.entities.enum import PaletteId

ForceFieldEntityData = Struct(
    "header" / EntityDataHeader,
    "type" / PaletteIdConstruct,
    "width" / FixedPoint,
    "height" / FixedPoint,
    "active" / Flag,
)


class ForceField(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return ForceFieldEntityData

    @property
    def type(self) -> PaletteId:
        return self._raw.data.type

    @type.setter
    def type(self, value: PaletteId) -> None:
        self._raw.data.type = value

    @property
    def width(self) -> float:
        return self._raw.data.width

    @width.setter
    def width(self, value: float) -> None:
        self._raw.data.width = value

    @property
    def height(self) -> float:
        return self._raw.data.height

    @height.setter
    def height(self, value: float) -> None:
        self._raw.data.height = value

    @property
    def active(self) -> bool:
        return self._raw.data.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.data.active = value
