import copy
import typing
from typing import Any, Self

import construct
from construct import (
    Aligned,
    Container,
    CString,
    Int16ul,
    Int32ul,
    ListContainer,
    Pointer,
    RepeatUntil,
    StopIf,
    Struct,
    this,
)

StringEntryHeader = Struct(
    "data_offset" / Int32ul,
    StopIf(this.data_offset == 0),
    "_string_offset" / Pointer(this.data_offset, Int32ul[2]),
    "_string_length" / Pointer(this.data_offset + 8, Int16ul[2]),
    "text" / Pointer(this._string_offset[0], Aligned(4, CString("utf-8"), pattern=b"\xbb")),
)

TextFileConstruct = Struct(
    "strings" / RepeatUntil(lambda string, lst, ctx: string.data_offset == 0, StringEntryHeader),
)


def num_bytes_to_align(length: int, modulus: int = 4) -> int:
    alignment = length % modulus
    if 0 < alignment < 4:
        return modulus - alignment
    else:
        return modulus


class MetroidHuntersTextFileAdapter(construct.Adapter):
    def __init__(self) -> None:
        super().__init__(TextFileConstruct)

    def _decode(self, obj: Container, context: Container, path: str) -> Container:
        decoded = copy.deepcopy(obj)

        # remove empty entry
        decoded.strings.pop()

        # wrap strings
        decoded.strings = ListContainer([StringEntry(string) for string in decoded.strings])

        return decoded

    def _encode(self, obj: Container, context: Container, path: str) -> Container:
        encoded = copy.deepcopy(obj)

        strings = typing.cast("list[StringEntry]", encoded.strings)

        # update sizes and offsets
        encoded.strings = ListContainer()

        data_offset = 2520
        _string_offset = 10068

        for string_wrapper in strings:
            string = string_wrapper._raw

            size = len(string_wrapper.text)
            if string._string_length[0] > size:
                size = string._string_length[0]

            string.data_offset = data_offset
            string._string_offset = ListContainer([_string_offset, _string_offset])
            string._string_length = ListContainer([size, size])

            data_offset += 12
            _string_offset += size + num_bytes_to_align(size)

            encoded.strings.append(string)

        # add empty entry
        encoded.strings.append(
            Container(
                {
                    "data_offset": 0,
                    "_string_offset": ListContainer([2520, 2532]),
                    "_string_length": ListContainer([2544, 0]),
                    "text": "T'",
                }
            )
        )

        return encoded


class StringEntry:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def __repr__(self) -> str:
        return f"<String data_offset={self.data_offset}> text={self.text}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StringEntry):
            return False
        return self.data_offset == other.data_offset and self.text == other.text

    @property
    def data_offset(self) -> int:
        return self._raw.data_offset

    @property
    def text(self) -> str:
        return self._raw.text

    @text.setter
    def text(self, value: str) -> None:
        self._raw.text = value


class MetroidHuntersTextFile:
    def __init__(self, raw: Container):
        self._raw = raw

    @classmethod
    def parse(cls, data: bytes) -> Self:
        # parse
        data = bytes(data)

        return cls(MetroidHuntersTextFileAdapter().parse(data))

    def build(self) -> bytes:
        # build
        data = MetroidHuntersTextFileAdapter().build(self._raw)

        return data

    def __eq__(self, value: Any) -> bool:
        return isinstance(value, MetroidHuntersTextFile) and self.strings == value.strings

    @property
    def strings(self) -> list[StringEntry]:
        return self._raw.strings

    @strings.setter
    def strings(self, value: list[StringEntry]) -> None:
        self._raw.strings = value

    def get_string(self, data_offset: int) -> StringEntry:
        string = next((string for string in self.strings if string.data_offset == data_offset), None)
        if string is None:
            raise ValueError(f"No string with data offset {data_offset} found!")
        return string
