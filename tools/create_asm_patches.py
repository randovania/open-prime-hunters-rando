from pathlib import Path

import keystone  # type: ignore[import-untyped]

this_folder = Path(__file__).parent
asm_sources = this_folder.joinpath("asm_sources")


def read_asm_file(file: str) -> str:
    return asm_sources.joinpath(file).read_text()


def create_asm_patch(code: str) -> bytes:
    assembler = keystone.Ks(keystone.KS_ARCH_ARM, keystone.KS_MODE_ARM + keystone.KS_MODE_LITTLE_ENDIAN)
    encoding, count = assembler.asm(code)
    return bytes(encoding)


def main():
    asm_patches: Path = this_folder.parent.joinpath("src", "open_prime_hunters_rando", "files", "asm_patches")

    asm_patches.mkdir(parents=True, exist_ok=True)

    for asm_source in asm_sources.glob("*.s"):
        try:
            code = create_asm_patch(read_asm_file(asm_source))
            Path(asm_patches / asm_source.with_suffix(".bin").name).write_bytes(code)

        except keystone.KsError as e:
            print(f"Error assembling {asm_source.name}: {e}")


if __name__ == "__main__":
    main()
