from collections.abc import Iterator
from typing import Self, SupportsIndex

from construct import Adapter, Construct, Container, Struct

from open_prime_hunters_rando.parsing.common_types import FixedPoint


class Vec2:
    raw: list[float]

    def __init__(self, *args: float) -> None:
        self.raw = list(args)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Vec2):
            return self.raw == value.raw
        else:
            return self.raw == value

    def __iter__(self) -> Iterator[float]:
        return iter(self.raw)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({repr(self.raw)[1:-1]})"

    def __getitem__(self, key: SupportsIndex) -> float:
        return self.raw[key]

    def __setitem__(self, key: SupportsIndex, value: float) -> None:
        self.raw[key] = value

    @property
    def x(self) -> float:
        return self.raw[0]

    @x.setter
    def x(self, value: float) -> None:
        self.raw[0] = value

    @property
    def y(self) -> float:
        return self.raw[1]

    @y.setter
    def y(self, value: float) -> None:
        self.raw[1] = value


class Vec3(Vec2):
    @property
    def z(self) -> float:
        return self.raw[2]

    @z.setter
    def z(self, value: float) -> None:
        self.raw[2] = value

    @property
    def r(self) -> float:
        return self.x

    @r.setter
    def r(self, value: float) -> None:
        self.x = value

    @property
    def g(self) -> float:
        return self.y

    @g.setter
    def g(self, value: float) -> None:
        self.y = value

    @property
    def b(self) -> float:
        return self.z

    @b.setter
    def b(self, value: float) -> None:
        self.z = value


class Vec4(Vec3):
    @property
    def w(self) -> float:
        return self.raw[3]

    @w.setter
    def w(self, value: float) -> None:
        self.raw[3] = value

    @property
    def a(self) -> float:
        return self.w

    @a.setter
    def a(self, value: float) -> None:
        self.w = value


class VectorAdapter(Adapter):
    def __init__(self, subcon: Construct, vec_type: type[Vec2], fields: tuple[str, ...]):
        super().__init__(subcon)
        self.vec_type = vec_type
        self.fields = fields

    @classmethod
    def for_n(cls, n: int) -> Self:
        fields: tuple[str, ...]
        vec_type: type[Vec2]
        match n:
            case 2:
                fields = ("x", "y")
                vec_type = Vec2
            case 3:
                fields = ("x", "y", "z")
                vec_type = Vec3
            case 4:
                fields = ("x", "y", "z", "w")
                vec_type = Vec4
            case _:
                raise ValueError(f"Invalid vector length {n}")

        return cls(
            Struct(
                *(field_name / FixedPoint for field_name in fields),
            ),
            vec_type,
            fields,
        )

    def _decode(self, obj: Container, context: Container, path: str) -> Vec2:
        return self.vec_type(*(obj[i] for i in self.fields))

    def _encode(self, obj: Vec2, context: Container, path: str) -> Container:
        container = Container()
        for i in self.fields:
            container[i] = getattr(obj, i)
        return container


Vector3Fx: VectorAdapter = VectorAdapter.for_n(3)
Vector4Fx: VectorAdapter = VectorAdapter.for_n(4)
