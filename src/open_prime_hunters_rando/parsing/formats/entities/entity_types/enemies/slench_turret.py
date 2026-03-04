from construct import Construct, Int32sl, Int32ul, Struct

from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, CollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields

SlenchTurretEntityData = Struct(
    "enemy_subtype" / Int32ul,
    "enemy_version" / Int32ul,
    "volume1" / CollisionVolume,
    "volume2" / CollisionVolume,
    "index" / Int32sl,
)


class SlenchTurret(EnemyFields, default_field_location="raw"):
    @classmethod
    def type_construct(cls) -> Construct:
        return SlenchTurretEntityData

    enemy_subtype = field(int)
    enemy_version = field(int)

    volume1 = field(BaseVolumeType)
    volume2 = field(BaseVolumeType)

    index = field(int)
