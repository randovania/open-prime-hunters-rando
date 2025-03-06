# Open Prime Hunters Rando
Open Source randomizer patcher for Metroid Prime Hunters. Currently supports patching the following:
- Pickups

## Usage

You will need to provide JSON data matching the [JSON schema](https://github.com/randovania/open-prime-hunters-rando/blob/main/src/open_prime_hunters_rando/files/schema.json) in order to successfully patch the game.

The patcher expects a path to an unmodified `.nds` file of Metroid Prime Hunters as well as the desired output directory. The patcher will create a modified `.nds` which can be used on any DS Emulator or flashcart.

With a JSON file:
`python -m open-prime-hunters-rando --input-path path/to/prime-hunters/file.nds --output-path path/to/the/output/directory --input-json path/to/patcher-config.json`

## Development
This repository uses [pre-commit](https://pre-commit.com/).
```
pip install pre-commit
pre-commit install
```
