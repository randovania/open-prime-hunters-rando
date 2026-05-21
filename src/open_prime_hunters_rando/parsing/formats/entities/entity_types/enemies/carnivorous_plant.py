import typing

from construct import Construct, Int16ul, Int32ul, Struct

from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, CollisionVolume, SphereVolumeType
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields, EnemyType

CarnivorousPlantEntityData = Struct(
    "enemy_health" / Int16ul,
    "enemy_damage" / Int16ul,
    "enemy_subtype" / Int32ul,
    "volume" / CollisionVolume,
)


class CarnivorousPlant(EnemyFields, default_field_location="raw"):
    @classmethod
    def type_construct(cls) -> Construct:
        return CarnivorousPlantEntityData

    enemy_health = field(int)
    enemy_damage = field(int)
    enemy_subtype = field(int)

    volume = field(BaseVolumeType)

    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.CARNIVOROUS_PLANT

    @classmethod
    def create(
        cls,
        enemy_health: int = 4,
        enemy_damage: int = 1,
        enemy_subtype: int = 37,
        volume: BaseVolumeType | None = None,
    ) -> typing.Self:
        if volume is None:
            volume = SphereVolumeType.create()

        carnivorous_plant = super().create()

        carnivorous_plant.enemy_health = enemy_health
        carnivorous_plant.enemy_damage = enemy_damage
        carnivorous_plant.enemy_subtype = enemy_subtype
        carnivorous_plant.volume = volume

        return carnivorous_plant
