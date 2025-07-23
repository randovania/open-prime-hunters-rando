import argparse
import json
import logging
import logging.config
import time
from pathlib import Path

from open_prime_hunters_rando import prime_hunters_patcher


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-path", required=True, type=Path, help="Path to an unmodified NDS rom of Metroid Prime Hunters."
    )
    parser.add_argument(
        "--output-path", required=True, type=Path, help="Path to where a modified NDS rom will be written to."
    )
    parser.add_argument(
        "--input-json", type=Path, help="Path to the configuration json. If missing, it's read from standard input"
    )
    parser.add_argument(
        "--export-parsed-files", type=bool, default=False, help="If true, exports the parsed entity files to a folder."
    )
    return parser


def setup_logging() -> None:
    handlers = {
        "default": {
            "level": "DEBUG",
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    }
    logging.config.dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] [%(levelname)s] [%(name)s] %(funcName)s: %(message)s",
                }
            },
            "handlers": handlers,
            "disable_existing_loggers": False,
            "loggers": {
                "default": {
                    "level": "DEBUG",
                },
            },
            "root": {
                "level": "DEBUG",
                "handlers": list(handlers.keys()),
            },
        }
    )
    logging.info("Hello world.")


def main() -> None:
    setup_logging()
    parser = create_parser()
    args = parser.parse_args()
    print(args)

    with args.input_json.open() as f:
        configuration = json.load(f)

    start = time.time()
    prime_hunters_patcher.patch_rom(
        args.input_path,
        args.output_path,
        configuration,
        args.export_parsed_files,
    )
    end = time.time()
    print(f"Patcher took {end - start:.03f} seconds")
