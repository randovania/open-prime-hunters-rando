import enum
import typing

from construct import Byte, Construct, Flag, Int16sl, Int16ul, Int32sl, Struct

from open_prime_hunters_rando.parsing.common_types import MessageConstruct
from open_prime_hunters_rando.parsing.common_types.vectors import Vec3
from open_prime_hunters_rando.parsing.construct_extensions import EnumAdapter
from open_prime_hunters_rando.parsing.formats.entities.base_entity import Entity
from open_prime_hunters_rando.parsing.formats.entities.entity_classes import field
from open_prime_hunters_rando.parsing.formats.entities.enum import EntityType, Message


class CameraSequenceId(enum.Enum):
    UNIT1_LAND_INTRO = 0
    UNIT2_LAND_INTRO = 1
    UNIT3_LAND_INTRO = 2
    UNIT4_LAND_INTRO = 3
    UNIT4_C1_PLATFORM_INTRO = 4
    UNIT2_CO_SCAN_INTRO = 5
    UNIT2_CO_SCAN_OUTRO = 6
    UNIT2_CO_BIT_INTRO = 7
    UNIT2_C4_TELEPORTER_INTRO = 8  # no file
    UNIT2_CO_BIT_OUTRO = 9
    UNIT2_CO_HELM_FLYBY = 10
    UNIT2_RM1_ARTIFACT_INTRO = 11
    UNIT2_RM1_ARTIFACT_OUTRO = 12
    UNIT2_C4_ARTIFACT_INTRO = 13
    UNIT2_C4_ARTIFACT_OUTRO = 14
    UNIT2_RM2_KANDEN_INTRO = 15
    UNIT2_RM3_ARTIFACT_INTRO = 16
    UNIT2_RM3_ARTIFACT_OUTRO = 17
    UNIT2_RM3_KANDEN_INTRO = 18
    UNIT4_CO_MORPHBALLMAZE = 19
    UNIT2_B1_OCTOLITH_INTRO = 20
    UNIT2_CO_GUARDIAN_INTRO = 21
    UNIT2_RM3_KANDEN_OUTRO = 22
    UNIT4_RM1_MORPHBALLJUMPS1 = 23
    UNIT4_LAND_GUARDIAN_INTRO = 24
    UNIT4_RM3_SCANDOOR_UNLOCK = 25
    UNIT1_C4_DROPMAZE_LEFT = 26
    UNIT4_CO_MORPHBALLMAZE_ENTER = 27
    UNIT4_RM5_ARCTICSPAWN_INTRO = 28
    UNIT4_RM5_ARCTICSPAWN_OUTRO = 29
    UNIT1_C4_DROPMAZE_RIGHT = 30
    UNIT4_RM3_HUNTERS_INTRO = 31
    UNIT4_RM3_HUNTERS_OUTRO = 32
    UNIT4_RM2_SWITCH_INTRO = 33
    UNIT4_RM2_GUARDIAN_INTRO = 34
    UNIT1_C5_PISTONMAZE_1 = 35
    UNIT1_C5_PISTONMAZE_2 = 36
    UNIT1_C5_PISTONMAZE_3 = 37
    UNIT1_C5_PISTONMAZE_4 = 38
    UNIT4_RM2_GUARDIAN_OUTRO = 39
    UNIT3_C2_MORPHBALLMAZE = 40
    UNIT4_RM5_POWERDOWN = 41
    UNIT4_RM1_MORPHBALLJUMPS2 = 42
    UNIT4_RM2_ELEVATOR_INTRO = 43
    UNIT4_RM1_MORPHBALLJUMPS3 = 44
    UNIT4_RM5_PILLARCRASH = 45
    UNIT4_RM1_WASP_INTRO = 46
    UNIT1_RM1_SPIRE_INTRO_LAYER0 = 47
    UNIT1_RM1_SPIRE_INTRO_LAYER3 = 48
    UNIT1_RM1_SPIRE_OUTRO = 49
    UNIT1_RM6_SPIRE_INTRO_LAYER3 = 50
    UNIT1_C1_SHIPFLYBY = 51
    UNIT4_RM3_TRACE_INTRO = 52
    UNIT3_RM1_FORCEFIELD_UNLOCK = 53
    UNIT3_RM1_SHIP_BATTLE_END = 54
    UNIT3_RM2_EVAC_INTRO = 55
    UNIT3_RM2_EVAC_FAIL = 56
    UNIT4_RM1_PUZZLE_ACTIVATE = 57
    UNIT4_RM1_ARTIFACT_INTRO = 58
    UNIT1_C0_WEAVEL_INTRO = 59
    BIGEYE_OCTOLITH_INTRO = 60
    UNIT2_RM4_PANEL_OPEN_1 = 61
    UNIT2_RM4_PANEL_OPEN_2 = 62
    UNIT2_RM4_PANEL_OPEN_3 = 63
    UNIT2_RM4_CNTLROOM_OPEN = 64
    UNIT2_RM4_TELEPORTER_ACTIVE = 65
    UNIT2_RM6_TELEPORTER_ACTIVE = 66  # no file
    UNIT1_RM2_RM3DOOR_OPEN = 67
    UNIT1_RM2_C3DOOR_OPEN = 68
    UNIT1_RM3_LAVADEMON_INTRO = 69  # no file
    UNIT1_RM3_MAGMAUL_INTRO = 70
    UNIT3_RM3_RACE1 = 71
    UNIT3_RM3_RACE1_FAIL = 72
    UNIT3_RM3_RACE2 = 73
    UNIT3_RM3_RACE2_FAIL = 74
    UNIT3_RM3_INCUBATOR_MALFUNCTION_INTRO = 75
    UNIT3_RM3_INCUBATOR_MALFUNCTION_OUTRO = 76
    UNIT3_RM3_DOOR_UNLOCK = 77
    UNIT1_RM3_FORCEFIELD_UNLOCK = 78
    UNIT4_RM4_SNIPERSPOT_INTRO = 79
    UNIT4_RM5_ARTIFACT_KEY_INTRO = 80
    UNIT4_RM5_ARTIFACT_INTRO = 81
    UNIT3_RM2_DOOR_UNLOCK = 82
    UNIT3_RM2_EVAC_END = 83
    UNIT1_RM3_FORCEFIELD_UNLOCK_DUP = 84  # duplicate of 78
    UNIT1_C0_WEAVEL_OUTRO = 85
    UNIT3_RM1_SYLUX_PRESHIP = 86
    UNIT1_RM1_MOVER_ACTIVATE_LAYER3 = 87
    UNIT3_RM1_SYLUX_INTRO = 88
    UNIT4_RM3_TRACE_OUTRO = 89
    UNIT4_RM5_SNIPER_INTRO = 90
    UNIT3_RM1_ARTIFACT_INTRO = 91
    UNIT1_RM6_SPIRE_ESCAPE = 92
    UNIT1_CRYSTALROOM_OCTOLITH = 93
    UNIT4_CO_MORPHBALLMAZE_EXIT = 94
    UNIT4_RM3_KEY_INTRO = 95
    UNIT2_RM1_DOOR_LOCK = 96
    UNIT2_RM1_KEY_INTRO = 97
    UNIT3_RM4_MORPHBALL = 98
    UNIT1_C0_MORPHBALL_DOOR_UNLOCK = 99
    UNIT1_RM6_FORCEFIELD_LOCK = 100
    UNIT1_RM6_FORCEFIELD_UNLOCK = 101
    UNIT1_LAND_COCKPIT = 102
    UNIT2_LAND_COCKPIT = 103
    UNIT3_LAND_COCKPIT = 104
    UNIT4_LAND_COCKPIT = 105
    UNIT1_LAND_COCKPIT_DUP = 106  # duplicate of 102
    UNIT1_RM1_ARTIFACT_INTRO = 107
    UNIT2_RM5_ARTIFACT_INTRO = 108
    UNIT2_C7_FORCEFIELD_LOCK = 109
    UNIT2_C7_FORCEFIELD_UNLOCK = 110
    UNIT2_C7_ARTIFACT_INTRO = 111
    UNIT2_RM8_ARTIFACT_INTRO = 112
    UNIT4_CO_DOOR_UNLOCK = 113
    UNIT1_LAND_COCKPIT_LAND = 114
    UNIT1_LAND_COCKPIT_TAKEOFF = 115
    UNIT2_LAND_COCKPIT_LAND = 116
    UNIT2_LAND_COCKPIT_TAKEOFF = 117
    UNIT3_LAND_COCKPIT_LAND = 118
    UNIT3_LAND_COCKPIT_TAKEOFF = 119
    UNIT4_LAND_COCKPIT_LAND = 120
    UNIT4_LAND_COCKPIT_TAKEOFF = 121
    UNIT1_LAND_COCKPIT_LAND_DUP = 122  # duplicate of 114
    UNIT1_LAND_COCKPIT_TAKEOFF_DUP = 123  # duplicate of 115
    UNIT1_RM2_MOVER1_ACTIVATE = 124
    UNIT1_RM2_MOVER2_ACTIVATE = 125
    UNIT1_RM2_MOVER3_ACTIVATE = 126
    UNIT3_RM3_RACE_ARTIFACT_INTRO = 127
    UNIT1_C5_ARTIFACT_INTRO = 128
    UNIT1_RM3_KEY_INTRO = 129
    UNIT1_RM3_ARTIFACT_INTRO = 130
    UNIT1_C3_ARTIFACT_INTRO = 131
    UNIT4_RM1_FORCEFIELD_UNLOCK = 132
    UNIT4_RM1_WASP_OUTRO = 133
    UNIT4_RM4_ARTIFACT_INTRO = 134
    UNIT4_RM4_ARTIFACT_OUTRO = 135
    UNIT3_RM2_ARTIFACT_INTRO = 136
    UNIT3_RM1_SHIP_INTRO = 137
    BIGEYE1_INTRO = 138
    UNIT4_RM2_KEY_INTRO = 139
    UNIT2_RM1_BIT_INTRO = 140
    UNIT1_RM1_SPIRE_ESCAPE = 141
    BIGEYE_MORPHBALL = 142
    UNIT3_RM3_KEY_OUTRO = 143
    UNIT3_RM4_KEY_INTRO = 144
    UNIT3_RM4_KEY_OUTRO = 145
    UNIT1_C0_KEY_INTRO = 146
    UNIT1_RM6_KEY_INTRO = 147
    UNIT1_RM6_MORPHBALL = 148
    UNIT3_RM1_BOTTOMFLOORKEY_INTRO = 149
    UNIT4_RM4_KEY_INTRO = 150
    UNIT4_RM4_GUARDIAN_OUTRO = 151
    UNIT4_RM5_FORCEFIELD_OUTRO = 152
    UNIT4_RM5_QUADTROID_OUTRO = 153
    UNIT4_RM2_KEY_OUTRO = 154
    UNIT3_RM4_GUARDIAN_INTRO = 155
    UNIT3_RM4_MORPHBALLDOOR_UNLOCK = 156
    UNIT2_RM5_KEY_INTRO = 157
    UNIT3_RM4_ITEM_INTRO = 158
    UNIT2_C7_KEY_INTRO = 159
    UNIT2_RM4_FORCEFIELD_UNLOCK_1 = 160
    UNIT2_RM4_FORCEFIELD_UNLOCK_2 = 161
    UNIT2_RM4_FORCEFIELD_UNLOCK_3 = 162
    UNIT3_C2_BATTLEHAMMER_INTRO = 163
    UNIT4_RM3_MORPHBALL_CAM = 164
    UNIT4_RM1_DOOR_OPEN = 165
    GOREA_B2_GUN_INTRO = 166
    GOREA_LAND_INTRO = 167
    GOREA_LAND_COCKPIT = 168
    GOREA_LAND_COCKPIT_LAND = 169
    GOREA_LAND_COCKPIT_TAKEOFF = 170
    UNIT4_RM1_PUZZLE_INTRO = 171
    MP00_INTRO = 172
    MP01_INTRO = 173
    MP02_INTRO = 174
    MP03_INTRO = 175
    MP04_INTRO = 176
    MP05_INTRO = 177
    MP06_INTRO = 178
    MP07_INTRO = 179
    MP08_INTRO = 180
    MP09_INTRO = 181
    MP10_INTRO = 182
    MP11_INTRO = 183
    MP12_INTRO = 184
    MP13_INTRO = 185
    MP14_INTRO = 186
    MP15_INTRO = 187
    MP16_INTRO = 188
    MP17_INTRO = 189
    MP18_INTRO = 190
    MP19_INTRO = 191
    MP20_INTRO = 192
    MP21_INTRO = 193
    MP22_INTRO = 194
    MP23_INTRO = 195
    MP24_INTRO = 196
    MP25_INTRO = 197
    MP26_INTRO = 198


CameraSequenceEntityData = Struct(
    "sequence_id" / EnumAdapter(CameraSequenceId, Byte),
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


class CameraSequence(Entity):
    @classmethod
    def type_construct(cls) -> Construct:
        return CameraSequenceEntityData

    sequence_id = field(int)

    handoff = field(bool)
    loop = field(bool)
    block_input = field(bool)

    force_alt_form = field(bool)
    force_biped_form = field(bool)

    delay_frames = field(int)

    player_id1 = field(int)
    player_id2 = field(int)

    entity1 = field(int)
    entity2 = field(int)

    end_message_target_id = field(int)
    end_message = field(Message)
    end_message_param = field(int)

    @classmethod
    def cls_entity_type(cls) -> EntityType:
        return EntityType.CAMERA_SEQUENCE

    @classmethod
    def create(
        cls,
        node_name: str = "",
        layer_state: typing.Sequence[bool] = (False,) * 16,
        entity_id: int = -1,
        position: Vec3 | tuple[float, float, float] = (0.0, 0.0, 0.0),
        up_vector: Vec3 | tuple[float, float, float] = (0.0, 1.0, 0.0),
        facing_vector: Vec3 | tuple[float, float, float] = (0.0, 0.0, 1.0),
        sequence_id: int = 0,
        handoff: bool = False,
        loop: bool = False,
        block_input: bool = True,
        force_alt_form: bool = False,
        force_biped_form: bool = True,
        delay_frames: int = 0,
        player_id1: int = 0,
        player_id2: int = 0,
        entity1: int = -1,
        entity2: int = -1,
        end_message_target_id: int = -1,
        end_message: Message = Message.NONE,
        end_message_param: int = 0,
    ) -> typing.Self:
        obj = super().create(
            node_name,
            layer_state,
            entity_id,
            position,
            up_vector,
            facing_vector,
        )
        obj.sequence_id = sequence_id
        obj.handoff = handoff
        obj.loop = loop
        obj.block_input = block_input
        obj.force_alt_form = force_alt_form
        obj.force_biped_form = force_biped_form
        obj.delay_frames = delay_frames
        obj.player_id1 = player_id1
        obj.player_id2 = player_id2
        obj.entity1 = entity1
        obj.entity2 = entity2
        obj.end_message_target_id = end_message_target_id
        obj.end_message = end_message
        obj.end_message_param = end_message_param

        return obj
