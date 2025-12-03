from construct import Container

from open_prime_hunters_rando.entities.entity_type import Message


class Artifact:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @property
    def model_id(self) -> int:
        return self._raw.model_id

    @model_id.setter
    def model_id(self, value: int) -> None:
        self._raw.model_id = value

    @property
    def artifact_id(self) -> int:
        return self._raw.artifact_id

    @artifact_id.setter
    def artifact_id(self, value: int) -> None:
        self._raw.artifact_id = value

    @property
    def active(self) -> bool:
        return self._raw.active

    @active.setter
    def active(self, value: bool) -> None:
        self._raw.active = value

    @property
    def has_base(self) -> bool:
        return self._raw.has_base

    @has_base.setter
    def has_base(self, value: bool) -> None:
        self._raw.has_base = value

    @property
    def message1_target(self) -> int:
        return self._raw.message1_target

    @message1_target.setter
    def message1_target(self, value: int) -> None:
        self._raw.message1_target = value

    @property
    def message1(self) -> Message:
        return self._raw.message1

    @message1.setter
    def message1(self, value: Message) -> None:
        self._raw.message1 = value

    @property
    def message2_target(self) -> int:
        return self._raw.message2_target

    @message2_target.setter
    def message2_target(self, value: int) -> None:
        self._raw.message2_target = value

    @property
    def message2(self) -> Message:
        return self._raw.message2

    @message2.setter
    def message2(self, value: Message) -> None:
        self._raw.message2 = value

    @property
    def message3_target(self) -> int:
        return self._raw.message3_target

    @message3_target.setter
    def message3_target(self, value: int) -> None:
        self._raw.message3_target = value

    @property
    def message3(self) -> Message:
        return self._raw.message3

    @message3.setter
    def message3(self, value: Message) -> None:
        self._raw.message3 = value

    @property
    def linked_entity_id(self) -> int:
        return self._raw.linked_entity_id

    @linked_entity_id.setter
    def linked_entity_id(self, value: int) -> None:
        self._raw.linked_entity_id = value
