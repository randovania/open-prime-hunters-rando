import enum

import construct
from construct import Construct, Container, Int32ul, Padded, Struct, Switch

from open_prime_hunters_rando.common import EnumAdapter, FixedPoint, Vec3
from open_prime_hunters_rando.entities.entity_file import Vector3Fx


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
    "type" / EnumAdapter(VolumeType, Int32ul),
    "data" / Padded(60, Switch(construct.this.type, volume_types)),
)


class BoxVolumeType:
    @property
    def box_vector1(self) -> Vec3:
        return self._raw.data.box_vector1

    @box_vector1.setter
    def box_vector1(self, value: Vec3) -> None:
        self._raw.data.box_vector1 = value

    @property
    def box_vector2(self) -> Vec3:
        return self._raw.data.box_vector2

    @box_vector2.setter
    def box_vector2(self, value: Vec3) -> None:
        self._raw.data.box_vector2 = value

    @property
    def box_vector3(self) -> Vec3:
        return self._raw.data.box_vector3

    @box_vector3.setter
    def box_vector3(self, value: Vec3) -> None:
        self._raw.data.box_vector3 = value

    @property
    def box_position(self) -> Vec3:
        return self._raw.data.box_position

    @box_position.setter
    def box_position(self, value: Vec3) -> None:
        self._raw.data.box_position = value

    @property
    def box_dot1(self) -> float:
        return self._raw.data.box_dot1

    @box_dot1.setter
    def box_dot1(self, value: float) -> None:
        self._raw.data.box_dot1 = value

    @property
    def box_dot2(self) -> float:
        return self._raw.data.box_dot2

    @box_dot2.setter
    def box_dot2(self, value: float) -> None:
        self._raw.data.box_dot2 = value

    @property
    def box_dot3(self) -> float:
        return self._raw.data.box_dot3

    @box_dot3.setter
    def box_dot3(self, value: float) -> None:
        self._raw.data.box_dot3 = value


class CylinderVolumeType:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def cylinder_vector(self) -> Vec3:
        return self._raw.data.cylinder_vector

    @cylinder_vector.setter
    def cylinder_vector(self, value: Vec3) -> None:
        self._raw.data.cylinder_vector = value

    @property
    def cylinder_position(self) -> Vec3:
        return self._raw.data.cylinder_position

    @cylinder_position.setter
    def cylinder_position(self, value: Vec3) -> None:
        self._raw.data.cylinder_position = value

    @property
    def cylinder_radius(self) -> float:
        return self._raw.data.cylinder_radius

    @cylinder_radius.setter
    def cylinder_radius(self, value: float) -> None:
        self._raw.data.cylinder_radius = value

    @property
    def cylinder_dot(self) -> float:
        return self._raw.data.cylinder_dot

    @cylinder_dot.setter
    def cylinder_dot(self, value: float) -> None:
        self._raw.data.cylinder_dot = value


class SphereVolumeType:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def sphere_position(self) -> Vec3:
        return self._raw.data.sphere_position

    @sphere_position.setter
    def sphere_position(self, value: Vec3) -> None:
        self._raw.data.sphere_position = value

    @property
    def sphere_radius(self) -> float:
        return self._raw.data.sphere_radius

    @sphere_radius.setter
    def sphere_radius(self, value: float) -> None:
        self._raw.data.sphere_radius = value


class VolumeTypeCommon:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @classmethod
    def type_construct(cls) -> Construct:
        return RawCollisionVolume

    @property
    def type(self) -> VolumeType:
        return self._raw.volume.type

    @type.setter
    def type(self, value: VolumeType) -> None:
        self._raw.volume.type = value

    def set_box(self) -> BoxVolumeType:
        return BoxVolumeType(self._raw.volume.data)

    def set_cylinder(self) -> CylinderVolumeType:
        return CylinderVolumeType(self._raw.volume.data)

    def set_sphere(self) -> SphereVolumeType:
        return SphereVolumeType(self._raw.volume.data)
