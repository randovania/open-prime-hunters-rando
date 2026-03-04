import copy
import typing
from collections.abc import Iterator
from typing import Any, Self

import construct
from construct import (
    Aligned,
    BitsSwapped,
    Bitwise,
    Container,
    Flag,
    Int16sl,
    Int16ul,
    Int32ul,
    ListContainer,
    Peek,
    Pointer,
    Rebuild,
    RepeatUntil,
    StopIf,
    Struct,
    Switch,
    this,
)

from open_prime_hunters_rando.parsing.common_types import DecodedString
from open_prime_hunters_rando.parsing.common_types.vectors import Vector3Fx
from open_prime_hunters_rando.parsing.construct_extensions import EnumAdapter
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_types.area_volume import AreaVolume
from open_prime_hunters_rando.parsing.formats.entities.entity_types.artifact import Artifact
from open_prime_hunters_rando.parsing.formats.entities.entity_types.camera_sequence import CameraSequence
from open_prime_hunters_rando.parsing.formats.entities.entity_types.defense_node import DefenseNode
from open_prime_hunters_rando.parsing.formats.entities.entity_types.door import Door
from open_prime_hunters_rando.parsing.formats.entities.entity_types.enemy_spawn import EnemySpawn
from open_prime_hunters_rando.parsing.formats.entities.entity_types.flag_base import FlagBase
from open_prime_hunters_rando.parsing.formats.entities.entity_types.force_field import ForceField
from open_prime_hunters_rando.parsing.formats.entities.entity_types.item_spawn import ItemSpawn
from open_prime_hunters_rando.parsing.formats.entities.entity_types.jump_pad import JumpPad
from open_prime_hunters_rando.parsing.formats.entities.entity_types.light_source import LightSource
from open_prime_hunters_rando.parsing.formats.entities.entity_types.morph_camera import MorphCamera
from open_prime_hunters_rando.parsing.formats.entities.entity_types.object import Object
from open_prime_hunters_rando.parsing.formats.entities.entity_types.octolith_flag import OctolithFlag
from open_prime_hunters_rando.parsing.formats.entities.entity_types.platform import Platform
from open_prime_hunters_rando.parsing.formats.entities.entity_types.player_spawn import PlayerSpawn
from open_prime_hunters_rando.parsing.formats.entities.entity_types.point_module import PointModule
from open_prime_hunters_rando.parsing.formats.entities.entity_types.teleporter import Teleporter
from open_prime_hunters_rando.parsing.formats.entities.entity_types.trigger_volume import TriggerVolume
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType

EntityTypeConstruct = EnumAdapter(EntityType, Int16ul)


EntityDataHeader = Struct(
    "entity_type" / EntityTypeConstruct,
    "entity_id" / Int16sl,
    "position" / Vector3Fx,
    "up_vector" / Vector3Fx,
    "facing_vector" / Vector3Fx,
)

raw_entry_fields = [
    "node_name" / DecodedString,
    "layer_state" / BitsSwapped(Bitwise(Flag[16])),
    "_size" / Int16ul,
    "_data_offset" / Int32ul,
]

RawEntityEntry = Struct(*raw_entry_fields)

entity_type_to_class: dict[EntityType, type[Entity]] = {
    EntityType.PLATFORM: Platform,
    EntityType.OBJECT: Object,
    EntityType.PLAYER_SPAWN: PlayerSpawn,
    EntityType.DOOR: Door,
    EntityType.ITEM_SPAWN: ItemSpawn,
    EntityType.ENEMY_SPAWN: EnemySpawn,
    EntityType.TRIGGER_VOLUME: TriggerVolume,
    EntityType.AREA_VOLUME: AreaVolume,
    EntityType.JUMP_PAD: JumpPad,
    EntityType.POINT_MODULE: PointModule,
    EntityType.MORPH_CAMERA: MorphCamera,
    EntityType.OCTOLITH_FLAG: OctolithFlag,
    EntityType.FLAG_BASE: FlagBase,
    EntityType.TELEPORTER: Teleporter,
    EntityType.DEFENSE_NODE: DefenseNode,
    EntityType.LIGHT_SOURCE: LightSource,
    EntityType.ARTIFACT: Artifact,
    EntityType.CAMERA_SEQUENCE: CameraSequence,
    EntityType.FORCE_FIELD: ForceField,
}

entity_type_to_construct = {etype: eclass.type_construct() for etype, eclass in entity_type_to_class.items()}

EntityEntry = Struct(
    *raw_entry_fields,
    StopIf(this._data_offset == 0),
    "_entity_type" / Rebuild(Peek(Pointer(this._data_offset, EntityTypeConstruct)), this.data.header.entity_type),
    "data"
    / Pointer(
        this._data_offset,
        Aligned(
            4,
            Struct(
                "header" / EntityDataHeader,
                "fields" / Switch(this._._entity_type, entity_type_to_construct),
            ),
        ),
    ),
)

EntityFileHeader = Struct(
    "version" / Int32ul,
    "layer_counts" / Int16ul[16],
)

EntityFileConstruct = Struct(
    "header" / EntityFileHeader,
    "entities" / RepeatUntil(lambda entity, lst, ctx: entity._data_offset == 0, EntityEntry),
)


def num_bytes_to_align(length: int, modulus: int = 4) -> int:
    if length % modulus > 0:
        return modulus - (length % modulus)
    return 0


class EntityAdapter(construct.Adapter):
    def __init__(self) -> None:
        super().__init__(EntityFileConstruct)

    def _decode(self, obj: Container, context: Container, path: str) -> Container:
        decoded = copy.deepcopy(obj)

        # remove empty entry
        decoded.entities.pop()

        # wrap entities
        decoded.entities = ListContainer(
            [entity_type_to_class[entity._entity_type](entity) for entity in decoded.entities]
        )

        return decoded

    def _encode(self, obj: Container, context: Container, path: str) -> Container:
        encoded = copy.deepcopy(obj)

        entities = typing.cast("list[Entity]", encoded.entities)

        # update sizes and offsets
        encoded.entities = ListContainer()

        offset = EntityFileHeader.sizeof()
        offset += RawEntityEntry.sizeof() * (len(entities) + 1)

        for entity_wrapper in entities:
            entity = entity_wrapper._raw

            size = entity_wrapper.size + EntityDataHeader.sizeof()
            entity._size = size
            entity._data_offset = offset

            offset += size + num_bytes_to_align(size)

            encoded.entities.append(entity)

        # add empty entry
        encoded.entities.append(
            Container(
                {
                    "node_name": "",
                    "layer_state": [False] * 16,
                    "_size": 0,
                    "_data_offset": 0,
                }
            )
        )

        return encoded


class EntityFile:
    def __init__(self, raw: Container):
        self._raw = raw

    @classmethod
    def parse(cls, data: bytes) -> Self:
        # align data to 4
        data = bytes(data) + b"\0" * num_bytes_to_align(len(data))

        return cls(EntityAdapter().parse(data))

    def build(self) -> bytes:
        # update layer counts
        for i in range(16):
            self._raw.header.layer_counts[i] = len(list(self.entities_for_layer(i)))

        # build
        data = EntityAdapter().build(self._raw)

        # remove unnecessary alignment bytes
        if self.entities:
            to_strip = num_bytes_to_align(self.entities[-1].size)
            if to_strip:
                data = data[:-to_strip]

        return data

    def __eq__(self, value: Any) -> bool:
        return isinstance(value, EntityFile) and self.version == value.version and self.entities == value.entities

    @property
    def version(self) -> int:
        return self._raw.header.version

    def entities_for_layer(self, layer: int) -> Iterator[Entity]:
        for entity in self.entities:
            if entity.layer_state[layer]:
                yield entity

    @property
    def entities(self) -> list[Entity]:
        return self._raw.entities

    @entities.setter
    def entities(self, value: list[Entity]) -> None:
        self._raw.entities = value

    def get_entity[T: Entity](
        self,
        entity_id: int,
        type_hint: type[T] = Entity,  # type: ignore[assignment]
    ) -> T:
        entity_idx = 0
        for entity in self.entities:
            if entity.size == 0:
                continue
            if entity.entity_id == entity_id:
                break
            entity_idx += 1
        else:
            raise ValueError(f"No entity with ID {entity_id} found!")

        assert isinstance(entity, type_hint)
        return entity

    def get_max_entity_id(self) -> int:
        entity_id = 0
        for entity in self.entities:
            if entity.entity_id > entity_id:
                entity_id = entity.entity_id
        return entity_id

    def append_entity(self, new_entity: Entity) -> int:
        new_entity_id = self.get_max_entity_id() + 1
        new_entity.entity_id = new_entity_id
        self.entities.append(new_entity)
        return new_entity_id

    def replace_entity(self, entity_id: int, new_entity: Entity, keep_old_transform: bool = True) -> None:
        index = next((i for i, entity in enumerate(self.entities) if entity.entity_id == entity_id), None)
        if index is None:
            raise ValueError(f"No entity with ID {entity_id} found!")
        new_entity.entity_id = entity_id
        old_entity = self.entities[index]
        new_entity.node_name = old_entity.node_name
        new_entity.layer_state = old_entity.layer_state

        if keep_old_transform:
            new_entity.position = old_entity.position
            new_entity.up_vector = old_entity.up_vector
            new_entity.facing_vector = old_entity.facing_vector

        self.entities[index] = new_entity
