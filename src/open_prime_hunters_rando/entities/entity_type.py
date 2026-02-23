from collections.abc import Collection
from typing import Any, Self

import construct
from construct import (
    Aligned,
    BitsSwapped,
    Bitwise,
    Byte,
    Container,
    Flag,
    Int16sl,
    Int16ul,
    Int32sl,
    Int32ul,
    ListContainer,
    Padded,
    PaddedString,
    Peek,
    Pointer,
    Rebuild,
    StopIf,
    Struct,
    Switch,
    this,
)

from open_prime_hunters_rando.common import EnumAdapter, FixedPoint, Rgb01, Vec3
from open_prime_hunters_rando.entities.enum import (
    DoorType,
    EnemyType,
    EntityType,
    Hunter,
    ItemType,
    Message,
    ObjectEffectFlags,
    ObjectFlags,
    PaletteId,
    PlatformFlags,
    TriggerVolumeFlags,
    TriggerVolumeType,
    VolumeType,
)

EntityTypeConstruct = EnumAdapter(EntityType, Int16ul)

Vector3Fx = Struct(
    "x" / FixedPoint,
    "y" / FixedPoint,
    "z" / FixedPoint,
)

Vector4Fx = Struct(
    "x" / FixedPoint,
    "y" / FixedPoint,
    "z" / FixedPoint,
    "w" / FixedPoint,
)

DecodedString = PaddedString(16, "ascii")

EntityDataHeader = Struct(
    "entity_type" / EntityTypeConstruct,
    "entity_id" / Int16sl,
    "position" / Vector3Fx,
    "up_vector" / Vector3Fx,
    "facing_vector" / Vector3Fx,
)

MessageConstruct = EnumAdapter(Message, Int32ul)

ItemTypeConstruct = EnumAdapter(ItemType, Int32sl)

PlatformEntityData = Struct(
    "header" / EntityDataHeader,
    "no_port" / Int32ul,
    "model_id" / Int32ul,
    "parent_id" / Int16sl,
    "active" / Flag,
    "delay" / Byte,
    "scan_data1" / Int16ul,
    "scan_message_target" / Int16sl,
    "scan_message" / MessageConstruct,
    "scan_data2" / Int16ul,
    "position_count" / Int16ul,
    "positions" / Vector3Fx[10],
    "rotations" / Vector4Fx[10],
    "position_offset" / Vector3Fx,
    "forward_speed" / FixedPoint,
    "backward_speed" / FixedPoint,
    "portal_name" / DecodedString,
    "movement_type" / Int32ul,
    "for_cutscene" / Int32ul,
    "reverse_type" / Int32ul,
    "flags" / construct.FlagsEnum(Int32ul, PlatformFlags),
    "contact_damage" / Int32ul,
    "beam_spawn_direction" / Vector3Fx,
    "beam_spawn_position" / Vector3Fx,
    "beam_id" / Int32sl,
    "beam_interval" / Int32ul,
    "beam_on_intervals" / Int32ul,
    "_unused1" / Int16ul,
    "_unused2" / Int16ul,
    "resist_effect_id" / Int32sl,
    "health" / Int32ul,
    "effectiveness" / Int32ul,
    "damage_effect_id" / Int32sl,
    "dead_effect_id" / Int32sl,
    "item_chance" / Byte,
    "_padding1" / Byte,
    "_padding2" / Int16ul,
    "item_type" / ItemTypeConstruct,
    "_unused3" / Int32ul,
    "_unused4" / Int32ul,
    "beam_hit_message_target" / Int32sl,
    "beam_hit_message" / MessageConstruct,
    "beam_hit_message_param1" / Int32sl,
    "beam_hit_message_param2" / Int32sl,
    "player_collision_message_target" / Int32sl,
    "player_collision_message" / MessageConstruct,
    "player_collision_message_param1" / Int32sl,
    "player_collision_message_param2" / Int32sl,
    "dead_message_target" / Int32sl,
    "dead_message" / MessageConstruct,
    "dead_message_param1" / Int32sl,
    "dead_message_param2" / Int32sl,
    "lifetime_message1_index" / Int16ul,
    "lifetime_message1_target" / Int16sl,
    "lifetime_message1" / MessageConstruct,
    "lifetime_message1_param1" / Int32sl,
    "lifetime_message1_param2" / Int32sl,
    "lifetime_message2_index" / Int16ul,
    "lifetime_message2_target" / Int16sl,
    "lifetime_message2" / MessageConstruct,
    "lifetime_message2_param1" / Int32sl,
    "lifetime_message2_param2" / Int32sl,
    "lifetime_message3_index" / Int16ul,
    "lifetime_message3_target" / Int16sl,
    "lifetime_message3" / MessageConstruct,
    "lifetime_message3_param1" / Int32sl,
    "lifetime_message3_param2" / Int32sl,
    "lifetime_message4_index" / Int16ul,
    "lifetime_message4_target" / Int16sl,
    "lifetime_message4" / MessageConstruct,
    "lifetime_message4_param1" / Int32sl,
    "lifetime_message4_param2" / Int32sl,
)

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

ObjectEntityData = Struct(
    "header" / EntityDataHeader,
    "flags" / construct.FlagsEnum(Byte, ObjectFlags),
    "_padding1" / Byte,
    "_padding2" / Int16ul,
    "effect_flags" / construct.FlagsEnum(Int32ul, ObjectEffectFlags),
    "model_id" / Int32sl,
    "linked_entity" / Int16sl,
    "scan_id" / Int16ul,
    "scan_message_target" / Int16sl,
    "_padding3" / Int16ul,
    "scan_message" / MessageConstruct,
    "effect_id" / Int32sl,
    "effect_interval" / Int32ul,
    "effect_on_inverals" / Int32ul,
    "effect_position_offset" / Vector3Fx,
    "volume" / RawCollisionVolume,
)

PlayerSpawnEntityData = Struct(
    "header" / EntityDataHeader,
    "availability" / Byte,
    "active" / Byte,
    "team_index" / Byte,
)

PaletteIdConstruct = EnumAdapter(PaletteId, Int32ul)

DoorEntityData = Struct(
    "header" / EntityDataHeader,
    "node_name" / DecodedString,
    "palette_id" / PaletteIdConstruct,
    "door_type" / EnumAdapter(DoorType, Int32ul),
    "connector_id" / Int32ul,
    "target_layer_id" / Byte,
    "locked" / Flag,
    "out_connector_id" / Byte,
    "out_loader_id" / Byte,
    "entity_file_name" / DecodedString,
    "room_name" / DecodedString,
)


ItemSpawnEntityData = Struct(
    "header" / EntityDataHeader,
    "parent_id" / Int32sl,
    "item_type" / ItemTypeConstruct,
    "enabled" / Flag,
    "has_base" / Flag,
    "always_active" / Flag,
    "_padding" / Byte,
    "max_spawn_count" / Int16ul,
    "spawn_interval" / Int16ul,
    "spawn_delay" / Int16ul,
    "notify_entity_id" / Int16sl,
    "collected_message" / MessageConstruct,
    "collected_message_param1" / Int32ul,
    "collected_message_param2" / Int32ul,
)

EnemyTypeConstruct = EnumAdapter(EnemyType, Byte)

HunterConstruct = EnumAdapter(Hunter, Int32ul)

WarWaspSpawnField = Struct(
    "volume0" / RawCollisionVolume,
    "volume1" / RawCollisionVolume,
    "volume2" / RawCollisionVolume,
    "movement_vectors" / Vector3Fx[16],
    "position_count" / Byte,
    "_padding1" / Byte,
    "_padding2" / Int16ul,
    "movement_type" / Int32ul,
)

EnemySpawnField0 = Struct(
    "volume0" / RawCollisionVolume,
    "volume1" / RawCollisionVolume,
    "volume2" / RawCollisionVolume,
    "volume3" / RawCollisionVolume,
)
EnemySpawnField1 = Struct(
    "data" / WarWaspSpawnField,
    "_padding1" / Int16ul,
    "_padding2" / Int16ul,
)
EnemySpawnField2 = Struct(
    "volume0" / RawCollisionVolume,
    "path_vector" / Vector3Fx,
    "volume1" / RawCollisionVolume,
    "volume2" / RawCollisionVolume,
)
EnemySpawnField3 = Struct(
    "volume0" / RawCollisionVolume,
    "_unused" / Int32ul[7],
    "facing" / Vector3Fx,
    "position" / Vector3Fx,
    "idle_range" / Vector3Fx,
)
EnemySpawnField4 = Struct(
    "volume0" / RawCollisionVolume,
    "_unused" / Int32ul[4],
    "position" / Vector3Fx,
    "weave_offset" / Int32ul,
    "field" / Int32sl,
)
EnemySpawnField5 = Struct(
    "enemy_subtype" / Int32ul,
    "volume0" / RawCollisionVolume,
    "volume1" / RawCollisionVolume,
    "volume2" / RawCollisionVolume,
    "volume3" / RawCollisionVolume,
)
EnemySpawnField6 = Struct(
    "enemy_subtype" / Int32ul,
    "enemy_version" / Int32ul,
    "volume0" / RawCollisionVolume,
    "volume1" / RawCollisionVolume,
    "volume2" / RawCollisionVolume,
    "volume3" / RawCollisionVolume,
)
EnemySpawnField7 = Struct(
    "enemy_health" / Int16ul,
    "enemy_damage" / Int16ul,
    "enemy_subtype" / Int32ul,
    "volume0" / RawCollisionVolume,
)
EnemySpawnField8 = Struct(
    "enemy_subtype" / Int32ul,
    "enemy_version" / Int32ul,
    "war_wasp" / WarWaspSpawnField,
)
EnemySpawnField9 = Struct(
    "hunter_id" / HunterConstruct,
    "encounter_type" / Int32ul,
    "hunter_weapon" / Int32ul,
    "hunter_health" / Int16ul,
    "hunter_health_max" / Int16ul,
    "field" / Int16ul,  # set in AI data
    "hunter_color" / Byte,
    "hunter_chance" / Byte,
)
EnemySpawnField10 = Struct(
    "enemy_subtype" / Int32ul,
    "enemy_version" / Int32ul,
    "volume0" / RawCollisionVolume,
    "volume1" / RawCollisionVolume,
    "index" / Int32sl,
)
EnemySpawnField11 = Struct(
    "sphere1_position" / Vector3Fx,
    "sphere1_radius" / FixedPoint,
    "sphere2_position" / Vector3Fx,
    "sphere2_radius" / FixedPoint,
)
EnemySpawnField12 = Struct(
    "field1" / Vector3Fx,
    "field2" / Int32ul,
    "field3" / Int32ul,
)

enemy_to_spawn_field = {
    EnemyType.ZOOMER: EnemySpawnField0,
    EnemyType.GEEMER: EnemySpawnField0,
    EnemyType.BLASTCAP: EnemySpawnField0,
    EnemyType.QUADTROID: EnemySpawnField0,
    EnemyType.CRASH_PILLAR: EnemySpawnField0,
    EnemyType.SLENCH: EnemySpawnField0,
    EnemyType.LESSER_ITHRAK: EnemySpawnField0,
    EnemyType.TROCRA: EnemySpawnField0,
    EnemyType.VOLDRUM2: EnemySpawnField0,
    EnemyType.WAR_WASP: EnemySpawnField1,
    EnemyType.SHRIEKBAT: EnemySpawnField2,
    EnemyType.TEMROID: EnemySpawnField3,
    EnemyType.PETRASYL1: EnemySpawnField3,
    EnemyType.PETRASYL2: EnemySpawnField4,
    EnemyType.PETRASYL3: EnemySpawnField4,
    EnemyType.PETRASYL4: EnemySpawnField4,
    EnemyType.CRETAPHID: EnemySpawnField5,
    EnemyType.GREATER_ITHRAK: EnemySpawnField5,
    EnemyType.ALIMBIC_TURRET: EnemySpawnField6,
    EnemyType.PSYCHO_BIT1: EnemySpawnField6,
    EnemyType.PSYCHO_BIT2: EnemySpawnField6,
    EnemyType.VOLDRUM1: EnemySpawnField6,
    EnemyType.FIRE_SPAWN: EnemySpawnField6,
    EnemyType.CARNIVOROUS_PLANT: EnemySpawnField7,
    EnemyType.BARBED_WAR_WASP: EnemySpawnField8,
    EnemyType.HUNTER: EnemySpawnField9,
    EnemyType.SLENCH_TURRET: EnemySpawnField10,
    EnemyType.GOREA1_A: EnemySpawnField11,
    EnemyType.GOREA2: EnemySpawnField12,
}

EnemySpawnEntityData = Struct(
    "header" / EntityDataHeader,
    "enemy_type" / EnemyTypeConstruct,
    "_padding1" / Byte,
    "_padding2" / Int16ul,
    "fields" / Padded(400, Switch(construct.this.enemy_type, enemy_to_spawn_field)),
    "linked_entity_id" / Int16sl,
    "spawn_limit" / Byte,
    "spawn_total" / Byte,
    "spawn_count" / Byte,
    "active" / Flag,
    "always_active" / Flag,
    "item_chance" / Byte,
    "spawner_health" / Int16ul,
    "cooldown_time" / Int16ul,
    "initial_cooldown" / Int16ul,
    "_padding3" / Int16ul,
    "active_distance" / FixedPoint,
    "enemy_active_distance" / FixedPoint,
    "node_name" / DecodedString,
    "entity_id1" / Int16sl,
    "_padding4" / Int16ul,
    "message1" / MessageConstruct,
    "entity_id2" / Int16sl,
    "_padding5" / Int16ul,
    "message2" / MessageConstruct,
    "entity_id3" / Int16sl,
    "_padding6" / Int16ul,
    "message3" / MessageConstruct,
    "item_type" / ItemTypeConstruct,
)

TriggerVolumeFlagsConstruct = construct.FlagsEnum(Int32ul, TriggerVolumeFlags)

TriggerVolumeEntityData = Struct(
    "header" / EntityDataHeader,
    "subtype" / EnumAdapter(TriggerVolumeType, Int32ul),
    "volume" / RawCollisionVolume,
    "_unused" / Int16ul,
    "active" / Flag,
    "always_active" / Flag,
    "deactivate_after_use" / Flag,
    "_padding1" / Byte,
    "repeat_delay" / Int16ul,
    "check_delay" / Int16ul,
    "required_state_bit" / Int16ul,
    "trigger_flags" / TriggerVolumeFlagsConstruct,
    "trigger_threshold" / Int32ul,
    "parent_id" / Int16sl,
    "_padding2" / Int16ul,
    "parent_message" / MessageConstruct,
    "parent_message_param1" / Int32sl,
    "parent_message_param2" / Int32sl,
    "child_id" / Int16sl,
    "_padding3" / Int16ul,
    "child_message" / MessageConstruct,
    "child_message_param1" / Int32sl,
    "child_message_param2" / Int32sl,
)

AreaVolumeEntityData = Struct(
    "header" / EntityDataHeader,
    "volume" / RawCollisionVolume,
    "_unused1" / Int16ul,
    "active" / Flag,
    "always_active" / Flag,
    "allow_mulitple" / Flag,
    "message_delay" / Byte,
    "_unused2" / Int16ul,
    "inside_message" / MessageConstruct,
    "inside_message_param1" / Int32sl,
    "inside_message_param2" / Int32sl,
    "parent_id" / Int16sl,
    "_padding3" / Int16ul,
    "exit_message" / MessageConstruct,
    "exit_message_param1" / Int32sl,
    "exit_message_param2" / Int32sl,
    "child_id" / Int16sl,
    "cooldown" / Int16ul,
    "priority" / Int32ul,
    "trigger_flags" / TriggerVolumeFlagsConstruct,
)

JumpPadEntityData = Struct(
    "header" / EntityDataHeader,
    "parent_id" / Int32sl,
    "_unused" / Int32ul,
    "volume" / RawCollisionVolume,
    "beam_vector" / Vector3Fx,
    "speed" / FixedPoint,
    "control_lock_time" / Int16ul,
    "cooldown_time" / Int16ul,
    "active" / Flag,
    "_padding1" / Byte,
    "_padding2" / Int16ul,
    "model_id" / Int32ul,
    "beam_type" / Int32ul,
    "trigger_flags" / TriggerVolumeFlagsConstruct,
)

PointModuleEntityData = Struct(
    "header" / EntityDataHeader,
    "next_id" / Int16sl,
    "prev_id" / Int16sl,
    "active" / Flag,
)

MorphCameraEntityData = Struct(
    "header" / EntityDataHeader,
    "volume" / RawCollisionVolume,
)

OctolithFlagEntityData = Struct(
    "header" / EntityDataHeader,
    "team_id" / Byte,
)

FlagBaseEntityData = Struct(
    "header" / EntityDataHeader,
    "team_id" / Int32ul,
    "volume" / RawCollisionVolume,
)

TeleporterEntityData = Struct(
    "header" / EntityDataHeader,
    "load_index" / Byte,
    "target_index" / Byte,
    "artifact_id" / Byte,
    "active" / Flag,
    "invisible" / Flag,
    "entity_filename" / PaddedString(15, "ascii"),
    "_unused" / Int16ul[2],
    "target_position" / Vector3Fx,
    "node_name" / DecodedString,
)

DefenseNodeEntityData = Struct(
    "header" / EntityDataHeader,
    "volume" / RawCollisionVolume,
)

ColorRgb = Struct(
    "red" / Rgb01,
    "green" / Rgb01,
    "blue" / Rgb01,
)

LightSourceEntityData = Struct(
    "header" / EntityDataHeader,
    "volume" / RawCollisionVolume,
    "light1_enabled" / Flag,
    "light1_color" / ColorRgb,
    "light1_vector" / Vector3Fx,
    "light2_enabled" / Flag,
    "light2_color" / ColorRgb,
    "light2_vector" / Vector3Fx,
)

ArtifactEntityData = Struct(
    "header" / EntityDataHeader,
    "model_id" / Byte,
    "artifact_id" / Byte,
    "active" / Flag,
    "has_base" / Flag,
    "message1_target" / Int16sl,
    "_padding1" / Int16ul,
    "message1" / MessageConstruct,
    "message2_target" / Int16sl,
    "_padding2" / Int16ul,
    "message2" / MessageConstruct,
    "message3_target" / Int16sl,
    "_padding3" / Int16ul,
    "message3" / MessageConstruct,
    "linked_entity_id" / Int16sl,
)

CameraSequenceEntityData = Struct(
    "header" / EntityDataHeader,
    "sequence_id" / Byte,
    "handoff" / Flag,
    "loop" / Flag,
    "block_input" / Flag,
    "force_alt_form" / Flag,
    "force_biped_form" / Flag,
    "delay_frames" / Int16ul,
    "player_id1" / Byte,
    "player_id2" / Byte,
    "entity1" / Int16sl,
    "entity2" / Int16sl,
    "end_message_target_id" / Int16sl,
    "end_message" / MessageConstruct,
    "end_message_param" / Int32sl,
)

ForceFieldEntityData = Struct(
    "header" / EntityDataHeader,
    "type" / PaletteIdConstruct,
    "width" / FixedPoint,
    "height" / FixedPoint,
    "active" / Flag,
)

types_to_construct = {
    EntityType.PLATFORM: PlatformEntityData,
    EntityType.OBJECT: ObjectEntityData,
    EntityType.PLAYER_SPAWN: PlayerSpawnEntityData,
    EntityType.DOOR: DoorEntityData,
    EntityType.ITEM_SPAWN: ItemSpawnEntityData,
    EntityType.ENEMY_SPAWN: EnemySpawnEntityData,
    EntityType.TRIGGER_VOLUME: TriggerVolumeEntityData,
    EntityType.AREA_VOLUME: AreaVolumeEntityData,
    EntityType.JUMP_PAD: JumpPadEntityData,
    EntityType.POINT_MODULE: PointModuleEntityData,
    EntityType.MORPH_CAMERA: MorphCameraEntityData,
    EntityType.OCTOLITH_FLAG: OctolithFlagEntityData,
    EntityType.FLAG_BASE: FlagBaseEntityData,
    EntityType.TELEPORTER: TeleporterEntityData,
    EntityType.DEFENSE_NODE: DefenseNodeEntityData,
    EntityType.LIGHT_SOURCE: LightSourceEntityData,
    EntityType.ARTIFACT: ArtifactEntityData,
    EntityType.CAMERA_SEQUENCE: CameraSequenceEntityData,
    EntityType.FORCE_FIELD: ForceFieldEntityData,
}

raw_entry_fields = [
    "node_name" / DecodedString,
    "layer_state" / BitsSwapped(Bitwise(Flag[16])),
    "_size" / Int16ul,
    "_data_offset" / Int32ul,
]

RawEntityEntry = Struct(*raw_entry_fields)

EntityEntry = Struct(
    *raw_entry_fields,
    StopIf(this._data_offset == 0),
    "_entity_type" / Rebuild(Peek(Pointer(this._data_offset, EntityTypeConstruct)), this.data.header.entity_type),
    "data" / Pointer(this._data_offset, Aligned(4, Switch(this._entity_type, types_to_construct))),
)


class Entity:
    def __init__(self, raw: Container) -> None:
        self._raw = raw

    @classmethod
    def create_from_template(
        cls, data: Container, node_name: str = "rmMain", active_layers: Collection[int] = tuple(range(16))
    ) -> Self:
        layer_state = [False] * 16
        for layer in active_layers:
            layer_state[layer] = False

        return cls(
            Container(
                {
                    "node_name": node_name,
                    "layer_state": ListContainer(layer_state),
                    "data": data,
                }
            )
        )

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        raise NotImplementedError

    @classmethod
    def create_header(
        cls,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
    ) -> Container:
        return Container(
            {
                "entity_type": cls.cls_entity_type(),
                "position": Container(position),
                "up_vector": Container(up_vector),
                "facing_vector": Container(facing_vector),
            }
        )

    @classmethod
    def create(
        cls,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
    ) -> Self:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<Entity type={self.entity_type} id={self.entity_id}>"

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, Entity):
            return False
        if value.node_name != self.node_name:
            return False
        for i in range(16):
            if value.layer_state(i) != self.layer_state(i):
                return False

        def check_container(container: dict, other: dict) -> bool:
            for k in container.keys() | other.keys():
                if k.startswith("_"):
                    continue
                if isinstance(container[k], dict):
                    if not isinstance(other[k], dict):
                        return False
                    if not check_container(container[k], other[k]):
                        return False
                else:
                    if container[k] != other[k]:
                        return False
            return True

        return check_container(self._raw, value._raw)

    @property
    def node_name(self) -> str:
        return self._raw.node_name

    @node_name.setter
    def node_name(self, value: str) -> None:
        self._raw.node_name = value

    @property
    def active_layers(self) -> tuple[int, ...]:
        return tuple(i for i in range(16) if self.layer_state(i))

    def layer_state(self, layer: int) -> bool:
        return self._raw.layer_state[layer]

    def set_layer_state(self, layer: int, state: bool) -> None:
        self._raw.layer_state[layer] = state

    @property
    def entity_type(self) -> EntityType:
        return self.header.entity_type

    @entity_type.setter
    def entity_type(self, value: EntityType) -> None:
        self.header.entity_type = value

    @property
    def entity_id(self) -> int:
        return self.header.entity_id

    @entity_id.setter
    def entity_id(self, value: int) -> None:
        self.header.entity_id = value

    @property
    def data(self) -> Container:
        return self._raw.data

    @data.setter
    def data(self, value: Container) -> None:
        self._raw.data = value

    @property
    def header(self) -> Container:
        return self.data.header

    @header.setter
    def header(self, value: Container) -> None:
        self.data.header = value

    @property
    def position(self) -> Vec3:
        return self.header.position

    @position.setter
    def position(self, value: Vec3) -> None:
        self.header.position = value

    @property
    def up_vector(self) -> Vec3:
        return self.header.up_vector

    @up_vector.setter
    def up_vector(self, value: Vec3) -> None:
        self.header.up_vector = value

    @property
    def facing_vector(self) -> Vec3:
        return self.header.facing_vector

    @facing_vector.setter
    def facing_vector(self, value: Vec3) -> None:
        self.header.facing_vector = value

    @property
    def type_construct(self) -> Struct:
        return types_to_construct[self.entity_type]

    @property
    def size(self) -> int:
        return self.type_construct.sizeof()
