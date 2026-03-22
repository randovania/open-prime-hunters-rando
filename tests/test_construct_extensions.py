from open_prime_hunters_rando.parsing.construct_extensions import ShortUtf8CString


def test_short_utf8_cstring():
    data = b"TTELEPATHISCHE BOTSCHAFT\\\xc0\xa6die schl\xc3\xbcssel sind allerorten\xc0\xa6"
    text = r"TTELEPATHISCHE BOTSCHAFT\…die schlüssel sind allerorten…"

    bytes_to_str = ShortUtf8CString()._bytes_to_str(data)
    assert bytes_to_str == text

    str_to_bytes = ShortUtf8CString()._str_to_bytes(text)
    assert str_to_bytes == data
