import logging
import typing
from pathlib import Path

from open_prime_hunters_rando.logger import LOG


def patch_with_status_update(
    input_path: Path,
    output_path: Path,
    configuration: dict,
    export_parsed_files: bool,
    status_update: typing.Callable[[float, str], None],
) -> None:
    from open_prime_hunters_rando.prime_hunters_patcher import patch_rom

    # messages depends on the layout but it is a good approximation
    total_logs = 80

    class StatusUpdateHandler(logging.Handler):
        count = 0

        def emit(self, record: logging.LogRecord) -> None:
            message = self.format(record)

            self.count += 1
            status_update(self.count / total_logs, message)

    new_handler = StatusUpdateHandler()
    new_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))

    try:
        LOG.setLevel(logging.INFO)
        LOG.handlers.insert(0, new_handler)
        LOG.propagate = False

        patch_rom(input_path, output_path, configuration)
        if new_handler.count < total_logs:
            status_update(1, f"Done was {new_handler.count}")

    finally:
        LOG.removeHandler(new_handler)
        LOG.propagate = True
