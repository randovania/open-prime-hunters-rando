from construct import Construct, Int32ul, Struct

from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, RawCollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemy_spawn import BaseEnemySpawn

TemroidPetrasyllEntityData = Struct(
    "volume" / RawCollisionVolume,
    "_unused" / Int32ul[7],
    "facing" / Vector3Fx,
    "position" / Vector3Fx,
    "idle_range" / Vector3Fx,
)


class TemroidPetrsyl1SpawnField(BaseEnemySpawn):
    @classmethod
    def type_construct(cls) -> Construct:
        return TemroidPetrasyllEntityData

    volume = field(BaseVolumeType)

    facing = field(Vec3)
    position = field(Vec3)

    idle_range = field(Vec3)
