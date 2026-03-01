from construct import Construct, Int16ul, Int32ul, Struct

from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, RawCollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemy_spawn import BaseEnemySpawn

CarnvirousPlantEntityData = Struct(
    "enemy_health" / Int16ul,
    "enemy_damage" / Int16ul,
    "enemy_subtype" / Int32ul,
    "volume" / RawCollisionVolume,
)


class CarnivorousPlantSpawnField(BaseEnemySpawn):
    @classmethod
    def type_construct(cls) -> Construct:
        return CarnvirousPlantEntityData

    enemy_health = field(int)
    enemy_damage = field(int)
    enemy_subtype = field(int)

    volume = field(BaseVolumeType)
