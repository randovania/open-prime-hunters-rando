from __future__ import annotations

from typing import Any

import construct
from construct import Adapter, Construct, Container, Enum, Int32ub, SizeofError, Subconstruct


class EnumAdapter(Adapter):
    def __init__(self, enum_class: Any, subcon: Any = Int32ub) -> None:
        super().__init__(Enum(subcon, enum_class))
        self._enum_class = enum_class

    def _decode(self, obj: str, context: Container, path: str) -> Enum:
        try:
            return self._enum_class[obj]
        except KeyError:
            return obj

    def _encode(self, obj: Enum, context: Container, path: str) -> str:
        if isinstance(obj, self._enum_class):
            return obj.name
        return obj


class ErrorWithMessage(Construct):
    def __init__(self, message: str, error: type[construct.ConstructError] = construct.ExplicitError) -> None:
        super().__init__()
        self.message = message
        self.flagbuildnone = True
        self.error = error

    def _parse(self, stream: bytes, context: Container, path: str) -> None:
        message = construct.evaluate(self.message, context)
        raise self.error(f"Error field was activated during parsing with error {message}", path=path)

    def _build(self, obj: None, stream: bytes, context: Container, path: str) -> None:
        message = construct.evaluate(self.message, context)
        raise self.error(f"Error field was activated during building with error {message}", path=path)

    def _sizeof(self, context: Container, path: str) -> None:
        raise construct.SizeofError("Error does not have size, because it interrupts parsing and building", path=path)


# ---------------------------------------------------------------------------
# ShortUtf8CString
#
# A Subconstruct that wraps CString("utf-8") and applies the shortened UTF-8
# codec on the raw bytes before decoding / after encoding.
#
# Parsing:  raw bytes from stream  ->  expand C0 xx -> E2 80 xx  ->  decode UTF-8
# Building: encode UTF-8  ->  compress E2 80 xx -> C0 xx  ->  write to stream
#
# Everything else (null terminator, alignment, pointer arithmetic) is handled
# by the surrounding Aligned / Pointer constructs and is not touched here.
# ---------------------------------------------------------------------------


class ShortUtf8CString(Subconstruct):
    r"""
    Null-terminated string using the shortened UTF-8 encoding.

    Wraps ``CString("utf-8")`` and intercepts the byte stream to apply the
    codec before the string is decoded:

    - On parse:  ``C0 xx``    ->  ``E2 80 xx``  (then decoded as UTF-8)
    - On build:  ``E2 80 xx`` ->  ``C0 xx``     (after encoding to UTF-8)

    Usage in a schema::

        "text" / ShortUtf8CString()

        # or inside Aligned / Pointer, exactly like a plain CString:
        "text" / Pointer(this.header._data_offset,
                     Aligned(4, ShortUtf8CString(), pattern=b"\xbb"))

    The parsed value is a plain Python ``str``.
    """

    def __init__(self) -> None:
        # CString handles null-termination; we only touch the payload bytes.
        super().__init__(construct.CString("utf-8"))

    # -- codec helpers -------------------------------------------------------

    @staticmethod
    def _bytes_to_str(data: bytes) -> str:
        """Expand shortened UTF-8 bytes to a Python str.

        C0 xx  ->  E2 80 xx, then decode as standard UTF-8.
        """
        out = bytearray()
        i = 0
        while i < len(data):
            if data[i] == 0xC0 and i + 1 < len(data):
                out += bytes([0xE2, 0x80, data[i + 1]])
                i += 2
            else:
                out.append(data[i])
                i += 1
        return out.decode("utf-8")

    @staticmethod
    def _str_to_bytes(text: str) -> bytes:
        """Encode a Python str to shortened UTF-8 bytes (without null terminator).

        Encode to standard UTF-8 first, then compress E2 80 xx  ->  C0 xx.
        """
        raw = text.encode("utf-8")
        out = bytearray()
        i = 0
        while i < len(raw):
            if raw[i] == 0xE2 and i + 2 < len(raw) and raw[i + 1] == 0x80:
                out += bytes([0xC0, raw[i + 2]])
                i += 3
            else:
                out.append(raw[i])
                i += 1
        return bytes(out)

    # -- Subconstruct protocol -----------------------------------------------
    # We override _parse / _build directly instead of _decode / _encode
    # because CString returns a str (post-decode), but we need to intercept
    # the raw bytes before any UTF-8 decoding takes place.

    def _parse(self, stream: bytes, context: Container, path: str) -> str:
        # Read raw shortened-UTF-8 bytes up to the null terminator.
        raw = bytearray()
        while True:
            b = construct.stream_read(stream, 1, path)
            if b == b"\x00":
                break
            raw += b
        return self._bytes_to_str(bytes(raw))

    def _build(self, obj: str, stream: bytes, context: Container, path: str) -> str:
        # Encode to shortened UTF-8 and append null terminator.
        encoded = self._str_to_bytes(obj) + b"\x00"
        construct.stream_write(stream, encoded, len(encoded), path)
        return obj

    def _sizeof(self, context: Container, path: str) -> None:
        raise SizeofError("ShortUtf8CString has no fixed size")
