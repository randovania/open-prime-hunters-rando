import random
from typing import NamedTuple

from construct import Container

from open_prime_hunters_rando.parsing.formats.entities.enum import Message


class NewTrigger(NamedTuple):
    area_name: str
    room_name: str
    active_layers: tuple[int, ...]
    entity_id: int
    artifact_messages: list[tuple[int, Message]]
    node_name: str = "rmMain"
    created_from_octolith: bool = False


def get_random_float() -> float:
    """
    Returns a random float
    """
    return float(random.randint(0, 255)) / 255


def create_rgb_values() -> Container:
    """
    Returns a container of RGB values
    """
    return Container(
        {
            "red": get_random_float(),
            "green": get_random_float(),
            "blue": get_random_float(),
        }
    )
