from typing import NamedTuple

from open_prime_hunters_rando.parsing.formats.entities.enum import Message


class NewTrigger(NamedTuple):
    area_name: str
    room_name: str
    active_layers: tuple[int, ...]
    entity_id: int
    artifact_messages: list[tuple[int, Message]]
    node_name: str = "rmMain"
