from __future__ import annotations

import os
from pathlib import Path

import pytest

from open_prime_hunters_rando.prime_hunters_patcher import DebugNintendoDsRom

_FAIL_INSTEAD_OF_SKIP = False


def get_env_or_skip(env_name):
    if env_name not in os.environ:
        if _FAIL_INSTEAD_OF_SKIP:
            pytest.fail(f"Missing environment variable {env_name}")
        else:
            pytest.skip(f"Skipped due to missing environment variable {env_name}")
    return os.environ[env_name]


@pytest.fixture(scope="session")
def rom_path():
    return Path(get_env_or_skip("PRIME_HUNTERS_PATH"))


@pytest.fixture(scope="session")
def rom(rom_path):
    return DebugNintendoDsRom.fromFile(rom_path)
