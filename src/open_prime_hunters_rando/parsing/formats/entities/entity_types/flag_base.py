import typing

from construct import Construct, Int32ul, Struct

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3
from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, BoxVolumeType, CollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType

FlagBaseEntityData = Struct(
    "team_id" / Int32ul,
    "volume" / CollisionVolume,
)


class FlagBase(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return FlagBaseEntityData

    team_id = field(int)

    volume = field(BaseVolumeType)

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.FLAG_BASE

    @classmethod
    def create(
        cls,
        node_name: str = "",
        layer_state: typing.Sequence[bool] = (False,) * 16,
        entity_id: int = -1,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 1.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 1.0),
        team_id: int = 0,
        volume: BaseVolumeType | None = None,
    ) -> typing.Self:
        if volume is None:
            volume = BoxVolumeType.create()

        obj = super().create(
            node_name,
            layer_state,
            entity_id,
            position,
            up_vector,
            facing_vector,
        )
        obj.team_id = team_id
        obj.volume = volume

        return obj
