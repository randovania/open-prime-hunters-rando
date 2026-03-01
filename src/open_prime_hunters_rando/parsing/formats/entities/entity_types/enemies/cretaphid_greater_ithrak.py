from construct import Construct, Int32ul, Struct

from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, CollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields

CretaphidGreaterIthrakEntityData = Struct(
    "enemy_subtype" / Int32ul,
    "volume1" / CollisionVolume,
    "volume2" / CollisionVolume,
    "volume3" / CollisionVolume,
    "volume4" / CollisionVolume,
)


class CretaphidGreaterIthrak(EnemyFields):
    @classmethod
    def type_construct(cls) -> Construct:
        return CretaphidGreaterIthrakEntityData

    enemy_subtype = field(int)

    volume1 = field(BaseVolumeType)
    volume2 = field(BaseVolumeType)
    volume3 = field(BaseVolumeType)
    volume4 = field(BaseVolumeType)
