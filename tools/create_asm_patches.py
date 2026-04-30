# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "keystone-engine>=0.9.2",
# ]
# ///

import re
from pathlib import Path

import keystone  # type: ignore[import-untyped]

this_folder = Path(__file__).parent
asm_sources = this_folder.joinpath("asm_sources")


def read_asm_file(file: str) -> str:
    return asm_sources.joinpath(file).read_text()


def create_asm_patch(raw_text: str, target_address: int) -> bytes:
    assembler = keystone.Ks(keystone.KS_ARCH_ARM, keystone.KS_MODE_ARM + keystone.KS_MODE_LITTLE_ENDIAN)
    encoding, count = assembler.asm(raw_text, target_address)
    return bytes(encoding)


def main():
    asm_patches: Path = this_folder.parent.joinpath("src", "open_prime_hunters_rando", "files", "asm_patches")

    asm_patches.mkdir(parents=True, exist_ok=True)

    for asm_source in asm_sources.glob("*.s"):
        raw_text = read_asm_file(asm_source)

        # Search the text for a custom @ADDRESS tag, necessary for relative jumps/loads
        match = re.search(r"@ADDRESS:\s*(0x[0-9a-fA-F]+)", raw_text)
        if match:
            target_address = int(match.group(1), 16)

            try:
                code = create_asm_patch(raw_text, target_address)
                Path(asm_patches / asm_source.with_suffix(".bin").name).write_bytes(code)

            except keystone.KsError as e:
                print(f"Error assembling {asm_source.name}: {e}")

        else:
            print(f"Warning: {asm_source.name} is missing an @ADDRESS tag.")


if __name__ == "__main__":
    main()
