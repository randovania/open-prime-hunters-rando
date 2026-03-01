import enum

from construct import Byte, Construct, Int16ul, Int32ul, Struct

from open_prime_hunters_rando.parsing.construct_extensions import EnumAdapter
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemy_spawn import BaseEnemySpawn


class Hunter(enum.Enum):
    SAMUS = 0
    KANDEN = 1
    TRACE = 2
    SYLUX = 3
    NOXUS = 4
    SPIRE = 5
    WEAVEL = 6
    GUARDIAN = 7
    RANDOM = 8


HunterConstruct = EnumAdapter(Hunter, Int32ul)


HunterEntityData = Struct(
    "hunter_id" / HunterConstruct,
    "encounter_type" / Int32ul,
    "hunter_weapon" / Int32ul,
    "hunter_health" / Int16ul,
    "hunter_health_max" / Int16ul,
    "field6" / Int16ul,  # set in AI data
    "hunter_color" / Byte,
    "hunter_chance" / Byte,
)


class HunterSpawnField(BaseEnemySpawn):
    @classmethod
    def type_construct(cls) -> Construct:
        return HunterEntityData

    hunter_id = field(Hunter)

    encounter_type = field(int)

    hunter_weapon = field(int)
    hunter_health = field(int)
    hunter_health_max = field(int)

    field6 = field(int)

    hunter_color = field(int)

    hunter_chance = field(int)
