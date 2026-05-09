import struct

import pytest

from open_prime_hunters_rando.patching.asm import bitfield_to_bytes, read_bytes_from_file
from open_prime_hunters_rando.patching.asm.asm_patches import (
    patch_ammo_per_expansion,
    patch_missile_launcher,
    patch_planets_and_artifacts,
    patch_starting_ammo,
    patch_starting_missiles,
)


def test_read_bytes():
    missile_launcher = read_bytes_from_file("missile_launcher.bin")
    assert missile_launcher == (
        b"\x01\xcc\x88\xe2\xb2%\xdc\xe18\x00\x9d\xe52 \x82\xe27\x10\xa0\xe3\x00\xe0\x9f\xe5\x1e\xff/\xe1T\xa3\x01\x02"
    )

    ammo_per_expansion = read_bytes_from_file("ammo_per_expansion.bin")
    assert ammo_per_expansion == b"\xff \x82\xe2"


@pytest.mark.parametrize(
    ("value", "expected_bytes"),
    [
        ("00000000", b"\x00"),
        ("01010101", b"\x55"),
        ("11111111", b"\xff"),
        ([False, False, False, False, False, False, False, False], b"\x00"),
        ([True, False, True, False, True, False, True, False], b"\xaa"),
        ([True, True, True, True, True, True, True, True], b"\xff"),
    ],
)
def test_bitfield_to_bytes(value, expected_bytes):
    bitfield = bitfield_to_bytes(value)
    assert bitfield == expected_bytes


def test_replace_missile_launcher_bytes():
    new_bytes = patch_missile_launcher(50)
    expected_bytes = (
        b"\x01\xcc\x88\xe2\xb2%\xdc\xe18\x00\x9d\xe5}/\x82\xe27\x10\xa0\xe3\x00\xe0\x9f\xe5\x1e\xff/\xe1T\xa3\x01\x02"
    )
    assert new_bytes == expected_bytes


@pytest.mark.parametrize(
    ("value", "expected_bytes"),
    [
        (10, b"d \x82\xe2"),
        (20, b"\xc8 \x82\xe2"),
        (60, b"\x96/\x82\xe2"),
        (102, b"\xff\x2f\x82\xe2"),
    ],
)
def test_replace_ammo_expansion_bytes(value, expected_bytes):
    new_bytes = patch_ammo_per_expansion(value)
    assert new_bytes == expected_bytes


@pytest.mark.parametrize(
    ("value", "expected_missile_bytes", "expected_ammo_bytes"),
    [
        (10, b"d\x80\xa0\xe3", b"d\x20\xa0\xe3"),
        (20, b"\xc8\x80\xa0\xe3", b"\xc8\x20\xa0\xe3"),
        (60, b"\x96\x8f\xa0\xe3", b"\x96\x2f\xa0\xe3"),
        (40, b"\x19\x8e\xa0\xe3", b"\x19\x2e\xa0\xe3"),
        (102, b"\xff\x8f\xa0\xe3", b"\xff\x2f\xa0\xe3"),
    ],
)
def test_replace_starting_ammo_bytes(value, expected_missile_bytes, expected_ammo_bytes):
    new_missile_bytes = patch_starting_missiles(value)
    assert new_missile_bytes == expected_missile_bytes

    new_ammo_bytes = patch_starting_ammo(value)
    assert new_ammo_bytes == expected_ammo_bytes


def test_patch_planets_and_artifacts():
    planets_dict = {
        "Arcterra": True,
        "Vesper Defense Outpost": False,
        "Celestial Archives": True,
        "Alinos": False,
    }
    planets_list = [
        planets_dict["Arcterra"],
        planets_dict["Arcterra"],
        planets_dict["Vesper Defense Outpost"],
        planets_dict["Vesper Defense Outpost"],
        planets_dict["Celestial Archives"],
        planets_dict["Celestial Archives"],
        planets_dict["Alinos"],
        planets_dict["Alinos"],
    ]
    planets_bytes = bitfield_to_bytes(planets_list) + b"\x10\xa0\xe3"
    assert planets_bytes == b"\xcc\x10\xa0\xe3"

    artifacts_dict = {
        "Arcterra": [0, 2],
        "Vesper Defense Outpost": [1, 0],
        "Celestial Archives": [1, 0],
        "Alinos": [2, 1],
    }
    artifacts_bitfield = "000011001000001000011001"
    as_hex = bitfield_to_bytes(artifacts_bitfield, "big").hex().zfill(8)
    artifacts_mask = struct.pack("<I", int(as_hex, 16))
    assert artifacts_mask == b"\x19\x82\x0c\x00"

    init_save_file = patch_planets_and_artifacts(planets_dict, artifacts_dict)
    assert init_save_file == (
        b"{\x90\xa0\xe3\x0f\x00\xa5\xe8\x0f\x00\xa5\xe8\x01\x90Y\xe2\xfb\xff\xff\x1a\x0f\x00\xa5\xe8\x03\x00\x85\xe8"
        b"\x00\x00\xa0\xe3\x00\x10\xa0\xe1\x000\xa0\xe1\x00\x90\xa0\xe1\x0f,\x84\xe2\xcc \x82\xe2\x0b\x02\xa2\xe8"
        b"\x0b\x02\xa2\xe8\x0b\x02\xa2\xe8\x0b\x02\xa2\xe8\x03\x00\x82\xe8P \x82\xe2\x0b\x02\xa2\xe8\x0b\x02\xa2\xe8"
        b"\x0b\x02\xa2\xe8\x0b\x02\xa2\xe8\x0b\x02\xa2\xe8\x0b\x02\xa2\xe8$\x00\x9f\xe5\x1c\x00\x84\xe5\xcc\x10\xa0"
        b"\xe3\xb2\x11\xc4\xe1\x180\x84\xe5\x01\x90\xa0\xe3\x1c B\xe2\tP\xa0\xe1\xa9q\x84\xe0\x00\xf0 \xe3\x00\xf0 "
        b"\xe3K\x10`\x00"
    )
