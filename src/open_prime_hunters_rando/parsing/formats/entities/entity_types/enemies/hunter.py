import enum
import typing

from construct import Byte, Construct, Int16ul, Int32ul, Struct

from open_prime_hunters_rando.parsing.construct_extensions import EnumAdapter
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemies.enemy_base import EnemyFields, EnemyType


class HunterType(enum.Enum):
    SAMUS = 0
    KANDEN = 1
    TRACE = 2
    SYLUX = 3
    NOXUS = 4
    SPIRE = 5
    WEAVEL = 6
    GUARDIAN = 7
    RANDOM = 8


HunterConstruct = EnumAdapter(HunterType, Int32ul)


HunterEntityData = Struct(
    "hunter_type" / HunterConstruct,
    "encounter_type" / Int32ul,
    "hunter_weapon" / Int32ul,
    "hunter_health" / Int16ul,
    "hunter_health_max" / Int16ul,
    "field6" / Int16ul,  # set in AI data
    "hunter_color" / Byte,
    "hunter_chance" / Byte,
)


class Hunter(EnemyFields, default_field_location="raw"):
    @classmethod
    def type_construct(cls) -> Construct:
        return HunterEntityData

    hunter_type = field(HunterType)

    encounter_type = field(int)

    hunter_weapon = field(int)
    hunter_health = field(int)
    hunter_health_max = field(int)

    field6 = field(int)

    hunter_color = field(int)

    hunter_chance = field(int)

    @classmethod
    def cls_enemy_type(cls) -> EnemyType:
        return EnemyType.HUNTER

    @classmethod
    def create(
        cls,
        hunter_type: HunterType = HunterType.SAMUS,
        encounter_type: int = 0,
        hunter_weapon: int = 0,
        hunter_health: int = 0,
        hunter_health_max: int = 0,
        field6: int = 1,
        hunter_color: int = 0,
        hunter_chance: int = 100,
    ) -> typing.Self:
        hunter = super().create()

        hunter.hunter_type = hunter_type
        hunter.encounter_type = encounter_type
        hunter.hunter_weapon = hunter_weapon
        hunter.hunter_health = hunter_health
        hunter.hunter_health_max = hunter_health_max
        hunter.field6 = field6
        hunter.hunter_color = hunter_color
        hunter.hunter_chance = hunter_chance

        return hunter
