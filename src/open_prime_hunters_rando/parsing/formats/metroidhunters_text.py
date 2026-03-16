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
    Struct,
    this,
)

TextEntryData = Struct(
    "string_offset" / Int32ul[2],
    "string_length" / Int16ul[2],
    "text" / Pointer(this.string_offset[0], Aligned(4, CString("utf8"), pattern=b"\xbb")),
)

TextEntryHeader = Struct(
    "data_offset" / Int32ul,
    "data" / Pointer(this.data_offset, TextEntryData),
)

TextFileConstruct = Struct(
    "strings" / RepeatUntil(lambda entity, lst, ctx: entity.data_offset == 0, TextEntryHeader),
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

        # wrap strings
        decoded.strings = ListContainer([TextEntry(string) for string in decoded.strings])

        return decoded

    def _encode(self, obj: Container, context: Container, path: str) -> Container:
        encoded = copy.deepcopy(obj)

        strings = typing.cast("list[TextEntry]", encoded.strings)

        # update sizes and offsets
        encoded.strings = ListContainer()

        data_offset = 2520
        string_offset = 10068

        for text_wrapper in strings:
            string = text_wrapper._raw

            size = len(text_wrapper.text)
            string.data_offset = data_offset
            string.data.string_offset = ListContainer([string_offset, string_offset])
            string.data.string_length = ListContainer([size, size])

            data_offset += 12
            string_offset += size + num_bytes_to_align(size)

            encoded.strings.append(string)

        return encoded


class TextEntry:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextEntry):
            return False
        return self.text == other.text

    @property
    def text(self) -> str:
        return self._raw.data.text

    @text.setter
    def text(self, value: str) -> None:
        self._raw.data.text = value


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
    def strings(self) -> list[TextEntry]:
        return self._raw.strings

    @strings.setter
    def strings(self, value: list[TextEntry]) -> None:
        self._raw.strings = value
