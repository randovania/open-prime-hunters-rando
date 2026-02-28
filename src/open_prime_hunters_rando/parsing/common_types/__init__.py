import math

import construct

from open_prime_hunters_rando.parsing.construct_extensions import EnumAdapter
from open_prime_hunters_rando.parsing.formats.entities.enum import ItemType, Message, PaletteId


class _FixedPointAdapter(construct.Adapter):
    def __init__(self, subcon: construct.Subconstruct, divisor: int):
        super().__init__(subcon)
        self.divisor = divisor

    def _decode(self, obj: int, context: dict, path: str) -> float:
        return float(obj) / self.divisor

    def _encode(self, obj: float, context: dict, path: str) -> int:
        return math.floor(obj * self.divisor)


FixedPoint = _FixedPointAdapter(construct.Int32sl, 4096)
"""Fixed-point number with 12-bit fractional part"""

Rgb01 = _FixedPointAdapter(construct.Byte, 255)
"""8-bit number within the interval [0.0, 1.0]"""

DecodedString = construct.PaddedString(16, "ascii")

MessageConstruct = EnumAdapter(Message, construct.Int32ul)
ItemTypeConstruct = EnumAdapter(ItemType, construct.Int32sl)
PaletteIdConstruct = EnumAdapter(PaletteId, construct.Int32ul)
