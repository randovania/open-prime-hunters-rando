import enum
from typing import Self

from construct import Construct, Container

from open_prime_hunters_rando.parsing.formats.entities.entity_classes import FieldsMixin


class EnemyType(enum.Enum):
    WAR_WASP = 0
    ZOOMER = 1
    TEMROID = 2
    PETRASYL1 = 3
    PETRASYL2 = 4
    PETRASYL3 = 5
    PETRASYL4 = 6
    UNKNOWN_7 = 7  # unused
    UNKNOWN_8 = 8  # unused
    UNKNOWN_9 = 9  # unused
    BARBED_WAR_WASP = 10
    SHRIEKBAT = 11
    GEEMER = 12
    UNKNOWN_13 = 13  # unused
    UNKNOWN_14 = 14  # unused
    UNKNOWN_15 = 15  # unused
    BLASTCAP = 16
    UNKNOWN_17 = 17  # unused
    ALIMBIC_TURRET = 18
    CRETAPHID = 19
    CRETAPHID_EYE = 20
    CRETAPHID_CRYSTAL = 21
    UNKNOWN_22 = 22  # unused (Cretaphid-related)
    PSYCHO_BIT1 = 23
    GOREA1_A = 24
    GOREA_HEAD = 25
    GOREA_ARM = 26
    GOREA_LEG = 27
    GOREA1_B = 28
    GOREA_SEAL_SPHERE1 = 29
    TROCRA = 30
    GOREA2 = 31
    GOREA_SEAL_SPHERE2 = 32
    GOREA_METEOR = 33
    PSYCHO_BIT2 = 34  # unused
    VOLDRUM2 = 35
    VOLDRUM1 = 36
    QUADTROID = 37
    CRASH_PILLAR = 38
    FIRE_SPAWN = 39
    SPAWNER = 40
    SLENCH = 41
    SLENCH_SHIELD = 42
    SLENCH_NEST = 43
    SLENCH_SYNAPSE = 44
    SLENCH_TURRET = 45
    LESSER_ITHRAK = 46
    GREATER_ITHRAK = 47
    HUNTER = 48
    FORCE_FIELD_LOCK = 49
    HIT_ZONE = 50  # used by 39/46/47
    CARNIVOROUS_PLANT = 51


class EnemyFields(FieldsMixin, default_field_location="raw"):
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @classmethod
    def type_construct(cls) -> Construct:
        raise NotImplementedError

    @classmethod
    def create(cls) -> Self:
        return cls(Container())
