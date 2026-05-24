import typing

from construct import Byte, Construct, Struct

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType

PlayerSpawnEntityData = Struct(
    "availability" / Byte,
    "active" / Byte,
    "team_index" / Byte,
)


class PlayerSpawn(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return PlayerSpawnEntityData

    availability = field(int)

    active = field(int)

    team_index = field(int)

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.PLAYER_SPAWN

    @classmethod
    def create(
        cls,
        node_name: str = "",
        layer_state: typing.Sequence[bool | int] = (False,) * 16,
        entity_id: int = -1,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 1.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 1.0),
        availability: int = 0,
        active: int = 0,
        team_index: int = 0,
    ) -> typing.Self:
        obj = super().create(
            node_name,
            layer_state,
            entity_id,
            position,
            up_vector,
            facing_vector,
        )
        obj.availability = availability
        obj.active = active
        obj.team_index = team_index

        return obj
