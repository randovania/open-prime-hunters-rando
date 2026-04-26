import pytest

from open_prime_hunters_rando.patching.asm import (
    patch_ammo_per_expansion,
    patch_missile_launcher,
    patch_starting_missiles,
    read_bytes_from_file,
)


def test_read_bytes():
    missile_launcher = read_bytes_from_file("missile_launcher.bin")
    assert missile_launcher == (
        b"\x01\xcc\x88\xe2\xb2%\xdc\xe18\x00\x9d\xe5\x05 \x82\xe27\x10\xa0\xe3"
        b"\n\xe0\xa0\xe3\x92\x0e\x02\xe0\x00\xe0\x9f\xe5\x1e\xff/\xe1T\xa3\x01\x02"
    )

    ammo_per_expansion = read_bytes_from_file("ammo_per_expansion.bin")
    assert ammo_per_expansion == b"\xff \x82\xe2"


def test_replace_missile_launcher_bytes():
    new_bytes = patch_missile_launcher(50)
    expected_bytes = (
        b"\x01\xcc\x88\xe2\xb2%\xdc\xe18\x00\x9d\xe5\x32 \x82\xe27\x10\xa0\xe3"
        b"\n\xe0\xa0\xe3\x92\x0e\x02\xe0\x00\xe0\x9f\xe5\x1e\xff/\xe1T\xa3\x01\x02"
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
    ("value", "expected_bytes"),
    [
        (10, b"d\x80\xa0\xe3"),
        (20, b"\xc8\x80\xa0\xe3"),
        (60, b"\x96\x8f\xa0\xe3"),
        (102, b"\xff\x8f\xa0\xe3"),
    ],
)
def test_replace_starting_missiles_bytes(value, expected_bytes):
    new_bytes = patch_starting_missiles(value)
    assert new_bytes == expected_bytes
