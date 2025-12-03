from construct import Container

from open_prime_hunters_rando.entities.entity_type import PaletteId


class ForceField:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def type(self) -> PaletteId:
        return self._raw.type

    @type.setter
    def type(self, value: PaletteId) -> None:
        self._raw.type = value

    @property
    def width(self) -> float:
        return self._raw.width

    @width.setter
    def width(self, value: float) -> None:
        self._raw.width = value

    @property
    def height(self) -> float:
        return self._raw.height

    @height.setter
    def height(self, value: float) -> None:
        self._raw.height = value

    @property
    def active(self) -> bool:
        return self._raw.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.active = value
