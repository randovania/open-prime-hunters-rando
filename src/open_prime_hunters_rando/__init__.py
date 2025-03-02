from pathlib import Path


def patch(input_path: Path, output_path: Path, configuration: dict) -> None:
    from .prime_hunters_patcher import patch_rom
    return patch_rom(input_path, output_path, configuration)
