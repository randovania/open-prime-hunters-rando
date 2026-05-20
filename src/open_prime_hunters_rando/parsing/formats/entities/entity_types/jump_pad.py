import typing

from construct import Construct, Flag, Int16ul, Int32sl, Int32ul, Padded, Struct

from open_prime_hunters_rando.parsing.common_types import FixedPoint
from open_prime_hunters_rando.parsing.common_types.vectors import Vec3, Vector3Fx
from open_prime_hunters_rando.parsing.common_types.volume import BaseVolumeType, BoxVolumeType, CollisionVolume
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.entity_types.trigger_volume import (
    TriggerVolumeFlags,
    TriggerVolumeFlagsConstruct,
)
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType

JumpPadEntityData = Struct(
    "parent_id" / Int32sl,
    "field1" / Int32ul,  # Unused
    "volume" / CollisionVolume,
    "beam_vector" / Vector3Fx,
    "speed" / FixedPoint,
    "control_lock_time" / Int16ul,
    "cooldown_time" / Int16ul,
    "active" / Padded(4, Flag),
    "model_id" / Int32ul,
    "beam_type" / Int32ul,
    "trigger_flags" / TriggerVolumeFlagsConstruct,
)


class JumpPad(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return JumpPadEntityData

    parent_id = field(int)

    field1 = field(int)

    volume = field(BaseVolumeType)

    beam_vector = field(Vec3)

    speed = field(int)
    control_lock_time = field(int)
    cooldown_time = field(int)

    active = field(bool)

    model_id = field(int)
    beam_type = field(int)

    trigger_flags = field(TriggerVolumeFlags)

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.JUMP_PAD

    @classmethod
    def create(
        cls,
        node_name: str = "",
        layer_state: typing.Sequence[bool] = (False,) * 16,
        entity_id: int = -1,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 1.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 1.0),
        parent_id: int = 65535,
        field1: int = 0,
        volume: BaseVolumeType | None = None,
        beam_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        speed: int = 0,
        control_lock_time: int = 0,
        cooldown_time: int = 0,
        active: bool = True,
        model_id: int = 0,
        beam_type: int = 0,
        trigger_flags: TriggerVolumeFlags = TriggerVolumeFlags.NONE,
    ) -> typing.Self:
        if volume is None:
            volume = BoxVolumeType.create()

        obj = super().create(
            node_name,
            layer_state,
            entity_id,
            position,
            up_vector,
            facing_vector,
        )
        obj.parent_id = parent_id
        obj.field1 = field1
        obj.volume = volume
        obj.beam_vector = Vec3(*beam_vector)
        obj.speed = speed
        obj.control_lock_time = control_lock_time
        obj.cooldown_time = cooldown_time
        obj.active = active
        obj.model_id = model_id
        obj.beam_type = beam_type
        obj.trigger_flags = trigger_flags

        return obj
