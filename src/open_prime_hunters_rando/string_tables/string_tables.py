import copy
from typing import Any, Self

import construct
from construct import (
    Container,
    If,
    Int16ul,
    Int32ul,
    PaddedString,
    Pointer,
    Struct,
    this,
)

raw_string_entry = [
    "string_id" / PaddedString(4, "ascii"),
    "data_offset" / Int32ul,
    "string_length" / Int16ul,
    "unk" / Int16ul,
]

RawStringEntry = Struct(*raw_string_entry)

Strings = Struct(
    *raw_string_entry,
    "string" / Pointer(this.data_offset, PaddedString(this.string_length, "ascii")),
)

StringTableConstruct = Struct(
    "entries" / Int32ul,
    "unk" / If(this.entries > 255, Int32ul),
    "strings" / Strings[this.entries],
)


def num_bytes_to_align(length: int, modulus: int = 4) -> int:
    if length % modulus > 0:
        return modulus - (length % modulus)
    return 0


class StringTableAdapter(construct.Adapter):
    def __init__(self) -> None:
        super().__init__(StringTableConstruct)

    def _decode(self, obj: Container, context: Container, path: str) -> Container:
        decoded = copy.deepcopy(obj)

        return decoded

    def _encode(self, obj: Container, context: Container, path: str) -> Container:
        encoded = copy.deepcopy(obj)

        return encoded


class StringTable:
    def __init__(self, raw: Container):
        self._raw = raw

    @classmethod
    def parse(cls, data: bytes) -> Self:
        # align data to 4
        data = bytes(data) + b"\0" * num_bytes_to_align(len(data))

        return cls(StringTableAdapter().parse(data))

    def build(self) -> bytes:
        # build
        data = StringTableAdapter().build(self._raw)

        return data

    def __eq__(self, value: Any) -> bool:
        return isinstance(value, StringTable)
