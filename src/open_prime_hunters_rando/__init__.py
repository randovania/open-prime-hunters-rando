from pathlib import Path

from .patch_util import patch_with_status_update


def patch(input_path: Path, output_path: Path, configuration: dict, export_parsed_files: bool) -> None:
    from .prime_hunters_patcher import patch_rom

    return patch_rom(input_path, output_path, configuration, export_parsed_files)


__all__ = [
    "patch",
    "patch_with_status_update",
]
