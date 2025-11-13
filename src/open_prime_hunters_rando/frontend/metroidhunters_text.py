import copy
from typing import Self

import construct
from construct import (
    Aligned,
    Container,
    CString,
    Int32ul,
    Struct,
)

aligned_cstring = Aligned(4, CString("utf8"), pattern=b"\xbb")

Characters = Struct(
    "name" / aligned_cstring,
    "alt_form" / aligned_cstring,
)

Strings = Struct(
    "multiplayer" / aligned_cstring[25],
    "multiplayer_bots" / aligned_cstring[7],
    "characters" / Characters[7],
    "naming?" / aligned_cstring[65],
    "file_completion" / aligned_cstring[7],
    "controls" / aligned_cstring[12],
    "file_creation?" / aligned_cstring[3],
    "credits" / aligned_cstring[32],
    "create_delete_file" / aligned_cstring[2],
    "download_play1" / aligned_cstring[2],
    "warnings_and_confirmations" / aligned_cstring[174],
    "advanced_options" / aligned_cstring[20],
    "erase_data" / aligned_cstring[2],
    "more_settings?" / aligned_cstring[14],
    "unk_group1" / aligned_cstring[2],
    "multiplayer_titles" / aligned_cstring[16],
    "unk_group2" / aligned_cstring[29],
    "multiplayer_maps" / aligned_cstring[28],
    "multiplayer_modes1" / aligned_cstring[7],
    "unk_group3" / aligned_cstring[171],
    "singleplayer_records" / aligned_cstring[4],
    "unk_group4" / aligned_cstring[29],
    "post_credits" / aligned_cstring[8],
    "unk_group5" / aligned_cstring[14],
    "multiplayer_mode_descriptions" / aligned_cstring[11],
    "file_collection" / aligned_cstring[3],
    "new_game_text" / aligned_cstring,
    "unk_number_group" / aligned_cstring[3],
    "singleplayer_records_title" / aligned_cstring,
    "singleplayer_title" / aligned_cstring[1],
    "download_play2" / aligned_cstring,
    "multiplayer_modes2" / aligned_cstring[2],
    "wifi_messages" / aligned_cstring[6],
    "copyright" / aligned_cstring[3],
    "unk_group6" / aligned_cstring[172],
    "abandon_game" / aligned_cstring[2],
    "error_messages" / aligned_cstring[36],
    "unk_group7" / aligned_cstring[130],
    "more_multiplayer_settings?" / aligned_cstring[20],
    "multiplayer_records?" / aligned_cstring[91],
)

TextConstruct = Struct(
    "unk" / Int32ul[2517],
    "strings" / Strings,
)


def num_bytes_to_align(length: int, modulus: int = 4) -> int:
    if length % modulus > 0:
        return modulus - (length % modulus)
    return 0


class MetroidHuntersTextFileAdapter(construct.Adapter):
    def __init__(self) -> None:
        super().__init__(TextConstruct)

    def _decode(self, obj: Container, context: Container, path: str) -> Container:
        decoded = copy.deepcopy(obj)

        return decoded

    def _encode(self, obj: Container, context: Container, path: str) -> Container:
        encoded = copy.deepcopy(obj)

        return encoded


class TextEntry:
    def __init__(self, raw: Container) -> None:
        self._raw = raw


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
