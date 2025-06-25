import copy
import enum
import typing
from typing import Any, Self

import construct
from construct import (
    Array,
    Container,
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


class ScanIcon(enum.Enum):
    NONE = 0
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
    "_data_offset" / Int32ul,
    "_string_length" / Int16ul,
    "scan_icon" / ScanIconConstruct,
]

RawStringEntry = Struct(*raw_string_entry)

Strings = Struct(
    *raw_string_entry,
    "text" / Pointer(this._data_offset, PaddedString(this._string_length, "ascii")),
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
    if length % modulus > 0:
        return modulus - (length % modulus)
    return 0


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

        offset = 8 if StringTableHeader.unk is not None else 4
        offset += RawStringEntry.sizeof() * len(strings)

        for string_wrapper in strings:
            string = string_wrapper._raw

            size = len(string_wrapper.text)
            string._string_length = size
            string._data_offset = offset

            offset += size + num_bytes_to_align(size)

            encoded.strings.append(string)

        return encoded


class StringEntry:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def __repr__(self) -> str:
        return f"<String string_id={self.string_id}> text={self.text}"

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, StringEntry):
            return False
        if value.string_id != self.string_id:
            return False

        def check_container(container: dict, other: dict) -> bool:
            for k in container.keys() | other.keys():
                if k.startswith("_"):
                    continue
                if isinstance(container[k], dict):
                    if not isinstance(other[k], dict):
                        return False
                    if not check_container(container[k], other[k]):
                        return False
                else:
                    if container[k] != other[k]:
                        return False
            return True

        return check_container(self._raw, value._raw)

    @property
    def string_id(self) -> str:
        return self._raw.string_id

    @string_id.setter
    def string_id(self, value: str) -> None:
        self._raw.string_id = value

    @property
    def scan_icon(self) -> ScanIcon:
        return self._raw.scan_icon

    @scan_icon.setter
    def scan_icon(self, value: ScanIcon) -> None:
        self._raw.scan_icon = value

    @property
    def text(self) -> str:
        return self._raw.text

    @text.setter
    def text(self, value: str) -> None:
        self._raw.text = value

    @property
    def string_length(self) -> int:
        return self._raw._string_length


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

        # remove unnecessary alignment bytes
        if self.strings:
            to_strip = num_bytes_to_align(self.strings[-1].string_length)
            if to_strip:
                data = data[:-to_strip]

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
        for string in self.strings:
            if string.string_id == string_id:
                break
        else:
            raise ValueError(f"No entity with ID {string_id} found!")
        return string
