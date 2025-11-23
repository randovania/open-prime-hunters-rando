import copy
import enum
import typing
from typing import Any, Self

import construct
from construct import (
    Aligned,
    Array,
    Byte,
    Container,
    CString,
    If,
    Int16ul,
    Int32ul,
    ListContainer,
    PaddedString,
    Pointer,
    Struct,
    this,
)

from open_prime_hunters_rando.constants import EnumAdapter


class ScanSpeed(enum.Enum):
    NONE = 0
    SLOW = 1
    MEDIUM = 2
    FAST = 3


ScanSpeedConstruct = EnumAdapter(ScanSpeed, Byte)


class ScanCategory(enum.Enum):
    NONE = ""
    BIOFORM = "B"
    EQUIPMENT = "E"
    LORE = "L"
    OBJECT = "O"
    OBJECT2 = "X"
    OBJECT3 = "o"
    SWITCH = "x"


ScanCategoryConstruct = EnumAdapter(ScanCategory, PaddedString(1, "utf-8"))

StringEntryHeader = Struct(
    "string_id" / PaddedString(4, "utf-8"),
    "_data_offset" / Int32ul,
    "_string_length" / Int16ul,
    "scan_speed" / ScanSpeedConstruct,
    "scan_category" / ScanCategoryConstruct,
)

Strings = Struct(
    "header" / StringEntryHeader,
    "text" / Pointer(this.header._data_offset, Aligned(4, CString("utf-8"), pattern=b"\xbb")),
)

StringTableHeader = Struct(
    "entries" / Int32ul,
    "unk" / If(this.entries > 255, Int32ul),
)

StringTableConstruct = Struct(
    "header" / StringTableHeader,
    "strings" / Array(this.header.entries, Strings),
)


def num_bytes_to_align(length: int, modulus: int = 4) -> int:
    alignment = length % modulus
    if 0 < alignment < 4:
        return modulus - alignment
    else:
        return modulus


class StringTableAdapter(construct.Adapter):
    def __init__(self) -> None:
        super().__init__(StringTableConstruct)

    def _decode(self, obj: Container, context: Container, path: str) -> Container:
        decoded = copy.deepcopy(obj)

        # wrap strings
        decoded.strings = ListContainer([StringEntry(string) for string in decoded.strings])

        return decoded

    def _encode(self, obj: Container, context: Container, path: str) -> Container:
        encoded = copy.deepcopy(obj)

        strings = typing.cast("list[StringEntry]", encoded.strings)

        # update sizes and offsets
        encoded.strings = ListContainer()

        offset = 8 if encoded.header.unk is not None else 4
        offset += StringEntryHeader.sizeof() * len(strings)

        for string_wrapper in strings:
            string = string_wrapper._raw

            size = len(string_wrapper.text)
            string.header._string_length = size
            string.header._data_offset = offset

            offset += size + num_bytes_to_align(size)

            encoded.strings.append(string)

        return encoded


class StringEntry:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def __repr__(self) -> str:
        return f"<String string_id={self.string_id}> text={self.text}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StringEntry):
            return False
        return (
            self.string_id == other.string_id
            and self.scan_speed == other.scan_speed
            and self.scan_category == other.scan_category
            and self.text == other.text
        )

    @property
    def string_id(self) -> str:
        return self._raw.header.string_id

    @string_id.setter
    def string_id(self, value: str) -> None:
        self._raw.header.string_id = value

    @property
    def scan_speed(self) -> ScanSpeed:
        return self._raw.header.scan_speed

    @scan_speed.setter
    def scan_speed(self, value: ScanSpeed) -> None:
        self._raw.header.scan_speed = value

    @property
    def scan_category(self) -> ScanCategory:
        return self._raw.header.scan_category

    @scan_category.setter
    def scan_category(self, value: ScanCategory) -> None:
        self._raw.header.scan_category = value

    @property
    def text(self) -> str:
        return self._raw.text

    @text.setter
    def text(self, value: str) -> None:
        self._raw.text = value


class StringTable:
    def __init__(self, raw: Container):
        self._raw = raw

    @classmethod
    def parse(cls, data: bytes) -> Self:
        # parse
        data = bytes(data)

        return cls(StringTableAdapter().parse(data))

    def build(self) -> bytes:
        # update amount of entries
        self._raw.header.entries = len(self.strings)

        # build
        data = StringTableAdapter().build(self._raw)

        return data

    def __eq__(self, value: Any) -> bool:
        return isinstance(value, StringTable) and self.strings == value.strings

    @property
    def entries(self) -> int:
        return self._raw.header.entries

    @property
    def strings(self) -> list[StringEntry]:
        return self._raw.strings

    @strings.setter
    def strings(self, value: list[StringEntry]) -> None:
        self._raw.strings = value

    def get_string(self, string_id: str) -> StringEntry:
        string = next((string for string in self.strings if string.string_id == string_id), None)
        if string is None:
            raise ValueError(f"No string with ID {string_id} found!")
        return string

    def get_group_max_string_id(self, string_group: str) -> str:
        string_id = "100"
        for string in self.strings:
            if string.string_id[-1] == string_group:
                string_id = string.string_id[:-1]
        return string_id

    def reverse_string(self, string: str) -> str:
        return string[::-1]

    def append_string(self, string_group: str, template: StringEntry) -> None:
        # Calculate the max string id of that string group
        max_string_id = self.get_group_max_string_id(string_group)

        # Reverse the string and convert it to an int to increment the max value
        new_max_id = str(int(self.reverse_string(max_string_id)) + 1)

        # Reverse the string again so the game can use it
        reversed_new_id = self.reverse_string(str(new_max_id).zfill(3))

        # Assign the new string id to the newly copied string
        new_string = copy.deepcopy(template)
        new_string.string_id = reversed_new_id + string_group

        # Add the new string to the string table
        self.strings.append(new_string)
