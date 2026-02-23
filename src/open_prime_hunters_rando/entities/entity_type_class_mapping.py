from open_prime_hunters_rando.entities.entity_type import Entity
from open_prime_hunters_rando.entities.entity_types.area_volume import AreaVolume
from open_prime_hunters_rando.entities.entity_types.artifact import Artifact
from open_prime_hunters_rando.entities.entity_types.camera_sequence import CameraSequence
from open_prime_hunters_rando.entities.entity_types.defense_node import DefenseNode
from open_prime_hunters_rando.entities.entity_types.door import Door
from open_prime_hunters_rando.entities.entity_types.enemy_spawn import EnemySpawn
from open_prime_hunters_rando.entities.entity_types.flag_base import FlagBase
from open_prime_hunters_rando.entities.entity_types.force_field import ForceField
from open_prime_hunters_rando.entities.entity_types.item_spawn import ItemSpawn
from open_prime_hunters_rando.entities.entity_types.jump_pad import JumpPad
from open_prime_hunters_rando.entities.entity_types.light_source import LightSource
from open_prime_hunters_rando.entities.entity_types.morph_camera import MorphCamera
from open_prime_hunters_rando.entities.entity_types.object import Object
from open_prime_hunters_rando.entities.entity_types.octolith_flag import OctolithFlag
from open_prime_hunters_rando.entities.entity_types.platform import Platform
from open_prime_hunters_rando.entities.entity_types.player_spawn import PlayerSpawn
from open_prime_hunters_rando.entities.entity_types.point_module import PointModule
from open_prime_hunters_rando.entities.entity_types.teleporter import Teleporter
from open_prime_hunters_rando.entities.entity_types.trigger_volume import TriggerVolume
from open_prime_hunters_rando.entities.enum import EntityType

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
