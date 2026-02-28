from __future__ import annotations

import enum
from typing import Self

import construct
from construct import Adapter, Container, Int32ul, Padded, Struct, Switch

from open_prime_hunters_rando.common import EnumAdapter, FixedPoint, Vec3
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_file import Vector3Fx


class TriggerVolumeFlags(enum.IntFlag):
    NONE = 0x0
    POWER_BEAM = 0x1
    VOLT_DRIVER = 0x2
    MISSILE = 0x4
    BATTLEHAMMER = 0x8
    IMPERIALIST = 0x10
    JUDICATOR = 0x20
    MAGMAUL = 0x40
    SHOCK_COIL = 0x80
    BEAM_CHARGED = 0x100
    PLAYER_BIPED = 0x200
    PLAYER_ALT = 0x400
    BIT_11 = 0x800  # unused
    INCLUDE_BOTS = 0x1000


TriggerVolumeFlagsConstruct = construct.FlagsEnum(Int32ul, TriggerVolumeFlags)


class VolumeType(enum.Enum):
    BOX = 0
    CYLINDER = 1
    SPHERE = 2


volume_types = {
    VolumeType.BOX: Struct(
        "box_vector1" / Vector3Fx,
        "box_vector2" / Vector3Fx,
        "box_vector3" / Vector3Fx,
        "box_position" / Vector3Fx,
        "box_dot1" / FixedPoint,
        "box_dot2" / FixedPoint,
        "box_dot3" / FixedPoint,
    ),
    VolumeType.CYLINDER: Struct(
        "cylinder_vector" / Vector3Fx,
        "cylinder_position" / Vector3Fx,
        "cylinder_radius" / FixedPoint,
        "cylinder_dot" / FixedPoint,
    ),
    VolumeType.SPHERE: Struct(
        "sphere_position" / Vector3Fx,
        "sphere_radius" / FixedPoint,
    ),
}
RawCollisionVolume = Struct(
    "volume_type" / EnumAdapter(VolumeType, Int32ul),
    "data"
    / Struct(
        "fields" / Padded(60, Switch(construct.this.type, volume_types)),
    ),
)


class CollisionVolume(Adapter):
    def __init__(self):
        super().__init__(RawCollisionVolume)

    def _decode(self, obj: Container, context: Container, path: str) -> VolumeType:
        match obj.volume_type:
            case VolumeType.BOX:
                cls = BoxVolumeType
            case VolumeType.CYLINDER:
                cls = CylinderVolumeType
            case VolumeType.SPHERE:
                cls = SphereVolumeType

        return cls(obj)

    def _encode(self, obj: VolumeType, context: Container, path: str) -> Container:
        return obj._raw


class BaseVolumeType:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    volume_type = field(VolumeType, "raw")

    @classmethod
    def create(cls) -> Self:
        return cls(Container({"data": Container({"fields": Container()})}))


class BoxVolumeType(BaseVolumeType):
    box_vector1 = field(Vec3)
    box_vector2 = field(Vec3)
    box_vector3 = field(Vec3)

    box_position = field(Vec3)

    box_dot1 = field(float)
    box_dot2 = field(float)
    box_dot3 = field(float)

    @classmethod
    def create(
        cls,
        box_vector1: Vec3,
        box_vector2: Vec3,
        box_vector3: Vec3,
        box_position: Vec3,
        box_dot1: float,
        box_dot2: float,
        box_dot3: float,
    ) -> Self:
        box = super().create()

        box.volume_type = VolumeType.BOX

        box.box_vector1 = box_vector1
        box.box_vector2 = box_vector2
        box.box_vector3 = box_vector3

        box.box_position = box_position

        box.box_dot1 = box_dot1
        box.box_dot2 = box_dot2
        box.box_dot3 = box_dot3

        return box


class CylinderVolumeType(BaseVolumeType):
    cylinder_vector = field(Vec3)
    cylinder_position = field(Vec3)
    cylinder_radius = field(float)
    cylinder_dot = field(float)

    @classmethod
    def create(
        cls, cylinder_vector: Vec3, cylinder_position: Vec3, cylinder_radius: float, cylinder_dot: float
    ) -> Self:
        cylinder = super().create()

        cylinder.volume_type = VolumeType.CYLINDER

        cylinder.cylinder_vector = cylinder_vector
        cylinder.cylinder_position = cylinder_position
        cylinder.cylinder_radius = cylinder_radius
        cylinder.cylinder_dot = cylinder_dot

        return cylinder


class SphereVolumeType(BaseVolumeType):
    sphere_position = field(Vec3)
    sphere_radius = field(float)

    @classmethod
    def create(cls, sphere_position: Vec3, sphere_radius: float) -> Self:
        sphere = super().create()

        sphere.volume_type = VolumeType.SPHERE

        sphere.sphere_position = sphere_position
        sphere.sphere_radius = sphere_radius

        return sphere
