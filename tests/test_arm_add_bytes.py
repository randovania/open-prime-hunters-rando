from open_prime_hunters_rando.patching.asm import generate_arm_add_bytes, read_bytes_from_file


def test_arm_add_bytes():
    original_launcher_bytes = read_bytes_from_file("missile_launcher.bin")
    assert original_launcher_bytes == (
        b"\x01\xcc\x88\xe2\xb2%\xdc\xe18\x00\x9d\xe5\x05 \x82\xe27\x10\xa0\xe3"
        b"\n\xe0\xa0\xe3\x92\x0e\x02\xe0\x00\xe0\x9f\xe5\x1e\xff/\xe1T\xa3\x01\x02"
    )

    launcher_instructions = generate_arm_add_bytes(50)
    new_bytes = original_launcher_bytes.replace(b"\x05\x20\x82\xe2", launcher_instructions)
    expected_bytes = (
        b"\x01\xcc\x88\xe2\xb2%\xdc\xe18\x00\x9d\xe5\x32 \x82\xe27\x10\xa0\xe3"
        b"\n\xe0\xa0\xe3\x92\x0e\x02\xe0\x00\xe0\x9f\xe5\x1e\xff/\xe1T\xa3\x01\x02"
    )
    assert expected_bytes == new_bytes

    original_ammo_bytes = read_bytes_from_file("ammo_per_expansion.bin")
    assert original_ammo_bytes == b"\xff \x82\xe2"

    expansion_instructions_1 = generate_arm_add_bytes(20, True)
    new_bytes = original_ammo_bytes.replace(b"\xff\x20\x82\xe2", expansion_instructions_1)
    expected_bytes = b"\xc8 \x82\xe2"
    assert expected_bytes == new_bytes

    expansion_instructions_2 = generate_arm_add_bytes(102, True)
    new_bytes = original_ammo_bytes.replace(b"\xff\x20\x82\xe2", expansion_instructions_2)
    expected_bytes = b"\xff\x2f\x82\xe2"
    assert expected_bytes == new_bytes
