import typing

from construct.lib import Container

from open_prime_hunters_rando.common import Vec3
from open_prime_hunters_rando.entities.entity import Entity
from open_prime_hunters_rando.entities.enum import EntityType, Message


class Artifact(Entity):
    @property
    def model_id(self) -> int:
        return self._raw.data.model_id

    @model_id.setter
    def model_id(self, value: int) -> None:
        self._raw.data.model_id = value

    @property
    def artifact_id(self) -> int:
        return self._raw.data.artifact_id

    @artifact_id.setter
    def artifact_id(self, value: int) -> None:
        self._raw.data.artifact_id = value

    @property
    def active(self) -> bool:
        return self._raw.data.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.data.active = value

    @property
    def has_base(self) -> bool:
        return self._raw.data.has_base

    @has_base.setter
    def has_base(self, value: bool) -> None:
        self._raw.data.has_base = value

    @property
    def message1_target(self) -> int:
        return self._raw.data.message1_target

    @message1_target.setter
    def message1_target(self, value: int) -> None:
        self._raw.data.message1_target = value

    @property
    def message1(self) -> Message:
        return self._raw.data.message1

    @message1.setter
    def message1(self, value: Message) -> None:
        self._raw.data.message1 = value

    @property
    def message2_target(self) -> int:
        return self._raw.data.message2_target

    @message2_target.setter
    def message2_target(self, value: int) -> None:
        self._raw.data.message2_target = value

    @property
    def message2(self) -> Message:
        return self._raw.data.message2

    @message2.setter
    def message2(self, value: Message) -> None:
        self._raw.data.message2 = value

    @property
    def message3_target(self) -> int:
        return self._raw.data.message3_target

    @message3_target.setter
    def message3_target(self, value: int) -> None:
        self._raw.data.message3_target = value

    @property
    def message3(self) -> Message:
        return self._raw.data.message3

    @message3.setter
    def message3(self, value: Message) -> None:
        self._raw.data.message3 = value

    @property
    def linked_entity_id(self) -> int:
        return self._raw.data.linked_entity_id

    @linked_entity_id.setter
    def linked_entity_id(self, value: int) -> None:
        self._raw.data.linked_entity_id = value

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.ARTIFACT

    @classmethod
    def create(
        cls,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        model_id: int = 0,
        artifact_id: int = 0,
        active: bool = True,
        has_base: bool = False,
        message1_target: int = 0,
        message1: Message = Message.NONE,
        message2_target: int = 0,
        message2: Message = Message.NONE,
        message3_target: int = 0,
        message3: Message = Message.NONE,
        linked_entity_id: int = 0,
    ) -> typing.Self:
        data = Container(
            {
                "header": cls.create_header(position, up_vector, facing_vector),
                "model_id": model_id,
                "artifact_id": artifact_id,
                "active": active,
                "has_base": has_base,
                "message1_target": message1_target,
                "_padding1": 0,
                "message1": message1,
                "message2_target": message2_target,
                "_padding2": 0,
                "message2": message2,
                "message3_target": message3_target,
                "_padding3": 0,
                "message3": message3,
                "linked_entity_id": linked_entity_id,
            }
        )
        return cls(Container({"data": data}))
