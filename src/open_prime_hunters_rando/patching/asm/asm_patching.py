from pathlib import Path

import keystone

NOP = bytes.fromhex("00F020E3")

asm_patches = Path(__file__).parent.joinpath("patches")


def read_asm_file(file: str) -> str:
    return asm_patches.joinpath(file).read_text()


def create_asm_patch(code: str) -> bytes:
    assembler = keystone.Ks(keystone.KS_ARCH_ARM, keystone.KS_MODE_ARM + keystone.KS_MODE_LITTLE_ENDIAN)
    encoding, count = assembler.asm(code)
    return bytes(encoding)
