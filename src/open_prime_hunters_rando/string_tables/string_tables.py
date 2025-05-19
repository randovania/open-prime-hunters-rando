import copy
import enum
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

from open_prime_hunters_rando.constants import EnumAdapter


class ScanIcon(enum.Enum):
    BIOFORM = 16897
    BIOFORM_BOSS = 16898
    BIOFORM3 = 16899
    EQUIPMENT = 17667
    LORE = 19459
    OBJECT = 20227
    OBJECT2 = 22531
    OBJECT3 = 28419
    SWITCH = 30723


ScanIconConstruct = EnumAdapter(ScanIcon, Int16ul)

raw_string_entry = [
    "string_id" / PaddedString(4, "ascii"),
    "data_offset" / Int32ul,
    "string_length" / Int16ul,
    "scan_icon" / ScanIconConstruct,
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


class StringEntry:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def string_id(self) -> str:
        return self._raw.string_id

    @string_id.setter
    def string_id(self, value: str) -> None:
        self._raw.string_id = value

    @property
    def scan_icon(self) -> str:
        return self._raw.scan_icon

    @scan_icon.setter
    def scan_icon(self, value: str) -> None:
        self._raw.scan_icon = value

    @property
    def string(self) -> str:
        return self._raw.string

    @string.setter
    def string(self, value: str) -> None:
        self._raw.string = value


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

    @property
    def entries(self) -> int:
        return self._raw.entries

    @property
    def strings(self) -> list[StringEntry]:
        return self._raw.strings

    @strings.setter
    def strings(self, value: list[StringEntry]) -> None:
        self._raw.strings = value

    def get_string(self, string_id: str) -> StringEntry:
        for string in self.strings:
            if string.string_id == string_id:
                break
        return string
