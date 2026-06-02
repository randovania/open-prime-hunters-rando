import pytest

from open_prime_hunters_rando.patching.asm import bitfield_to_bytes, create_bitmask, read_bytes_from_file
from open_prime_hunters_rando.patching.asm.asm_patches import (
    patch_ammo_per_expansion,
    patch_missile_launcher,
    patch_planets_and_artifacts,
    patch_starting_ammo,
    patch_starting_energy,
    patch_starting_missiles,
    patch_starting_weapons,
)


def test_read_bytes():
    missile_launcher = read_bytes_from_file("missile_launcher.bin")
    assert missile_launcher == (
        b"\x00\xf0 \xe3\x00\xf0 \xe3\x01\x0c\x88\xe2\xb2\x15\xd0\xe12\x10\x81\xe2\xb2\x15\xc0\xe1\xb2\xe5\xd0\xe1\xbe"
        b"\x94\xd0\xe1\t\x90N\xe0\xb6\x95\xc0\xe1\xb2\xb5\xd0\xe1 \x00\x9f\xe5\xbc\xb0\xc0\xe1\x02\x90\xa0\xe3\x06\x00"
        b"\x00\xea\x00\xf0 \xe3\x00\xf0 \xe3\x00\xf0 \xe3\x00\xf0 \xe3\x00\xf0 \xe3\x00\xf0 \xe3\x10\x97\x0e\x02"
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
    new_bytes = patch_missile_launcher(50, 0x020E9730)
    expected_bytes = (
        b"\x00\xf0 \xe3\x00\xf0 \xe3\x01\x0c\x88\xe2\xb2\x15\xd0\xe1}\x1f\x81\xe2\xb2\x15\xc0\xe1\xb2\xe5\xd0\xe1\xbe"
        b"\x94\xd0\xe1\t\x90N\xe0\xb6\x95\xc0\xe1\xb2\xb5\xd0\xe1 \x00\x9f\xe5\xbc\xb0\xc0\xe1\x02\x90\xa0\xe3\x06\x00"
        b"\x00\xea\x00\xf0 \xe3\x00\xf0 \xe3\x00\xf0 \xe3\x00\xf0 \xe3\x00\xf0 \xe3\x00\xf0 \xe3\x10\x97\x0e\x02"
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
        "alinos_1": "011",
        "alinos_2": "001",
        "celestial_archives_1": "001",
        "celestial_archives_2": "000",
        "vesper_defense_outpost_1": "001",
        "vesper_defense_outpost_2": "000",
        "arcterra_1": "000",
        "arcterra_2": "011",
    }

    artifacts_bitmask = create_bitmask("011000000001000001001011")
    assert artifacts_bitmask == b"K\x10`\x00"

    init_save_file = patch_planets_and_artifacts(planets_dict, artifacts_dict)
    assert init_save_file == (
        b"{\x90\xa0\xe3\x0f\x00\xa5\xe8\x0f\x00\xa5\xe8\x01\x90Y\xe2\xfb\xff\xff\x1a\x0f\x00\xa5\xe8\x03\x00\x85\xe8"
        b"\x00\x00\xa0\xe3\x00\x10\xa0\xe1\x000\xa0\xe1\x00\x90\xa0\xe1\x0f,\x84\xe2\xcc \x82\xe2\x0b\x02\xa2\xe8\x0b"
        b"\x02\xa2\xe8\x0b\x02\xa2\xe8\x0b\x02\xa2\xe8\x03\x00\x82\xe8P \x82\xe2\x0b\x02\xa2\xe8\x0b\x02\xa2\xe8\x0b"
        b"\x02\xa2\xe8\x0b\x02\xa2\xe8\x0b\x02\xa2\xe8\x0b\x02\xa2\xe8$\x00\x9f\xe5\x1c\x00\x84\xe5\xcc\x10\xa0\xe3"
        b"\xb2\x11\xc4\xe1\x180\x84\xe5\x01\x90\xa0\xe3\x1c B\xe2\tP\xa0\xe1\xa9q\x84\xe0\x00\xf0 "
        b"\xe3\x00\xf0 \xe3K\x10`\x00"
    )


def test_patch_starting_weapons():
    weapons_dict = {
        "battlehammer": False,
        "imperialist": True,
        "judicator": True,
        "magmaul": False,
        "missile_launcher": True,
        "shock_coil": True,
        "volt_driver": True,
    }

    assert patch_starting_weapons(weapons_dict) == b"\xb7"


@pytest.mark.parametrize(
    ("value", "expected_bytes"),
    [
        (1, b"\x01\x00\x00\x00"),
        (99, b"c\x00\x00\x00"),
        (300, b",\x01\x00\x00"),
        (1299, b"\x13\x05\x00\x00"),
    ],
)
def test_patch_starting_energy(value, expected_bytes):
    assert patch_starting_energy(value) == expected_bytes
