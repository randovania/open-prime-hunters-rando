import json
from pathlib import Path

from ndspy.rom import NintendoDSRom

room_name_to_entity_file = [
    # Room ID, Area Name, Room Name, Enitity File
    (0, "Alinos", "Connector X", None),
    (2, "Alinos", "Connector Z", None),
    (4, "Alinos", "Morph Connector X", None),
    (6, "Alinos", "Morph Connector Z", None),
    (8, "Celestial Archives", "Connector X", "unit2_CX"),
    (10, "Celestial Archives", "Connector Z", "unit2_CZ"),
    (12, "Vesper Defense Outpost", "Connector X", "unit3_CX"),
    (14, "Vesper Defense Outpost", "Connector Z", "unit3_CZ"),
    (16, "Arcterra", "Connector X", None),
    (18, "Arcterra", "Connector Z", None),
    # (20, "Alinos", "Connector CX", "unit1_CX"),
    # (21, "Alinos", "Connector CX", "unit1_CX"),
    (22, "Alinos", "Small Connector X", None),
    (24, "Oubliette", "Connector Z", None),
    (25, "Vesper Defense Outpost", "Morph Connector Z", None),
    (27, "Alinos", "Alinos Gateway", "Unit1_Land"),
    (28, "Alinos", "Echo Hall", "Unit1_C0"),
    (29, "Alinos", "High Ground", "unit1_RM1"),
    (30, "Alinos", "Magma Drop", "Unit1_C4"),
    (31, "Alinos", "Elder Passage", "unit1_RM6"),
    (32, "Alinos", "Alimbic Cannon Control Room", "crystalroom"),
    (33, "Alinos", "Combat Hall", "unit1_rm4"),
    (34, "Alinos", "Stronghold Void B", "Unit1_TP1"),
    (35, "Alinos", "Biodefense Chamber B", "Unit1_b1"),
    (36, "Alinos", "Alimbic Gardens", "Unit1_C1"),
    (37, "Alinos", "Thermal Vast", "Unit1_C2"),
    (38, "Alinos", "Piston Cave", "Unit1_C5"),
    (39, "Alinos", "Alinos Perch", "unit1_RM2"),
    (40, "Alinos", "Council Chamber", "unit1_rm3"),
    (41, "Alinos", "Processor Core", "unit1_rm5"),
    (42, "Alinos", "Crash Site", "Unit1_C3"),
    (43, "Alinos", "Stronghold Void A", "Unit1_TP2"),
    (44, "Alinos", "Biodefense Chamber A", "Unit1_b2"),
    (45, "Celestial Archives", "Celestial Gateway", "unit2_Land"),
    (46, "Celestial Archives", "Helm Room", "unit2_C0"),
    (47, "Celestial Archives", "Meditation Room", "unit2_C1"),
    (48, "Celestial Archives", "Data Shrine 01", "unit2_RM1"),
    (49, "Celestial Archives", "Fan Room Alpha", "unit2_C2"),
    (50, "Celestial Archives", "Data Shrine 02", "unit2_RM2"),
    (51, "Celestial Archives", "Fan Room Beta", "unit2_C3"),
    (52, "Celestial Archives", "Data Shrine 03", "unit2_RM3"),
    (53, "Celestial Archives", "Synergy Core", "unit2_C4"),
    (54, "Celestial Archives", "Stronghold Void A", "Unit2_TP1"),
    (55, "Celestial Archives", "Biodefense Chamber A", "Unit2_b1"),
    (56, "Celestial Archives", "Tetra Vista", "Unit2_C6"),
    (57, "Celestial Archives", "New Arrival Registration", "Unit2_C7"),
    (58, "Celestial Archives", "Transfer Lock", "Unit2_RM4"),
    (59, "Celestial Archives", "Incubation Vault 01", "Unit2_RM5"),
    (60, "Celestial Archives", "Incubation Vault 02", "Unit2_RM6"),
    (61, "Celestial Archives", "Incubation Vault 03", "Unit2_RM7"),
    (62, "Celestial Archives", "Docking Bay", "unit2_RM8"),
    (63, "Celestial Archives", "Stronghold Void B", "Unit2_TP2"),
    (64, "Celestial Archives", "Biodefense Chamber B", "Unit2_b2"),
    (65, "Vesper Defense Outpost", "VDO Gateway", "unit3_Land"),
    (66, "Vesper Defense Outpost", "Bioweaponry Lab", "unit3_C0"),
    (67, "Vesper Defense Outpost", "Cortex CPU", "Unit3_C2"),
    (68, "Vesper Defense Outpost", "Weapons Complex", "Unit3_RM1"),
    (69, "Vesper Defense Outpost", "Compression Chamber", "unit3_rm4"),
    (70, "Vesper Defense Outpost", "Stronghold Void A", "Unit3_TP1"),
    (71, "Vesper Defense Outpost", "Biodefense Chamber A", "Unit3_b1"),
    (72, "Vesper Defense Outpost", "Ascension", "unit3_C1"),
    (73, "Vesper Defense Outpost", "Fuel Stack", "Unit3_RM2"),
    (74, "Vesper Defense Outpost", "Stasis Bunker", "Unit3_RM3"),
    (75, "Vesper Defense Outpost", "Stronghold Void B", "Unit3_TP2"),
    (76, "Vesper Defense Outpost", "Biodefense Chamber B", "Unit3_b2"),
    (77, "Arcterra", "Arcterra Gateway", "unit4_Land"),
    (78, "Arcterra", "Ice Hive", "Unit4_RM1"),
    (79, "Arcterra", "Sic Transit", "unit4_rm3"),
    (80, "Arcterra", "Frost Labyrinth", "unit4_C0"),
    (81, "Arcterra", "Stronghold Void B", "Unit4_TP1"),
    (82, "Arcterra", "Biodefense Chamber B", "unit4_b1"),
    (83, "Arcterra", "Drip Moat", "unit4_C1"),
    (84, "Arcterra", "Subterranean", "Unit4_RM2"),
    (85, "Arcterra", "Sanctorus", "unit4_rm4"),
    (86, "Arcterra", "Fault Line", "Unit4_RM5"),
    (87, "Arcterra", "Stronghold Void A", "Unit4_TP2"),
    (88, "Arcterra", "Biodefense Chamber B", "unit4_b2"),
    (89, "Oubliette", "Oubliette Gateway", "Gorea_Land"),
    (90, "Oubliette", "Oubliette Storage ", "Gorea_Peek"),
    (91, "Oubliette", "Gorea Arena A", "Gorea_b1"),
    (92, "Oubliette", "Gorea Arena B", "gorea_b2"),
]


def _get_all_entity_files(rom: NintendoDSRom) -> list:
    files = rom.filenames
    # Entity files
    entity_files = []
    for i in range(1065, 1070):
        entity_files.append(files[i])
    for i in range(1090, 1159):
        entity_files.append(files[i])

    return entity_files


def get_entity_data(rom: NintendoDSRom, export_path: Path) -> dict:
    all_entity_files = _get_all_entity_files(rom)

    entities_per_area: dict = {
        "Alinos": {},
        "Celestial Archives": {},
        "Vesper Defense Outpost": {},
        "Arcterra": {},
        "Oubliette": {},
    }
    for entity_file in all_entity_files:
        file = rom.getFileByName(entity_file)

        if "_dm" in entity_file:
            continue
        if "unit3_rm5" in entity_file:
            continue

        entry_length = 0x18
        entry_start = 0x24
        entry_end = 0x3C

        num_entities = file[0x04]

        entity_dict: dict = {}

        for i in range(num_entities + 1):
            entity_entry = file[entry_start:entry_end]
            data_offset = int.from_bytes(entity_entry[0x14:0x16], "little")

            entity_type = file[data_offset]
            entity_id = file[data_offset + 2]

            position = {
                "x": int.from_bytes(file[data_offset + 4 : data_offset + 8], "little", signed=True) / 4096.0,
                "y": int.from_bytes(file[data_offset + 8 : data_offset + 12], "little", signed=True) / 4096.0,
                "z": int.from_bytes(file[data_offset + 12 : data_offset + 16], "little", signed=True) / 4096.0,
            }

            up_vector = {
                "x": int.from_bytes(file[data_offset + 16 : data_offset + 20], "little", signed=True) / 4096.0,
                "y": int.from_bytes(file[data_offset + 20 : data_offset + 24], "little", signed=True) / 4096.0,
                "z": int.from_bytes(file[data_offset + 24 : data_offset + 28], "little", signed=True) / 4096.0,
            }

            facing_vector = {
                "x": int.from_bytes(file[data_offset + 28 : data_offset + 32], "little", signed=True) / 4096.0,
                "y": int.from_bytes(file[data_offset + 32 : data_offset + 36], "little", signed=True) / 4096.0,
                "z": int.from_bytes(file[data_offset + 36 : data_offset + 40], "little", signed=True) / 4096.0,
            }

            entity_type_data: dict = {}

            # Player Spawn
            if entity_type == 2:
                entity_type_data["availabilty"] = file[data_offset + 40]
                entity_type_data["active"] = bool(file[data_offset + 41])
            # Door
            if entity_type == 3:
                entity_type_data["node_name"] = str(file[data_offset + 40 : data_offset + 56], "utf-8").strip("\u0000")
                entity_type_data["palette_id"] = int.from_bytes(file[data_offset + 56 : data_offset + 60], "little")
                entity_type_data["door_type"] = int.from_bytes(file[data_offset + 60 : data_offset + 64], "little")
                entity_type_data["connector_id"] = int.from_bytes(file[data_offset + 64 : data_offset + 68], "little")
                entity_type_data["target_layer_id"] = file[data_offset + 69]
                entity_type_data["locked"] = bool(file[data_offset + 70])
                entity_type_data["out_connector_id"] = file[data_offset + 71]
                entity_type_data["out_loader_id"] = file[data_offset + 72]
                entity_type_data["entity_filename"] = str(file[data_offset + 72 : data_offset + 88], "utf-8").strip(
                    "\u0000"
                )
                entity_type_data["room_name"] = str(file[data_offset + 72 : data_offset + 88], "utf-8").strip("\u0000")
            # Item Spawn
            if entity_type == 4:
                item_type = file[data_offset + 44]
                # Refills
                # if item_type in [0, 1, 2, 12, 13, 14, 15, 16, 19]:
                #     continue
                entity_type_data["item_type"] = item_type
                entity_type_data["enabled"] = bool(file[data_offset + 48])
                entity_type_data["has_base"] = bool(file[data_offset + 49])
                entity_type_data["always_active"] = bool(file[data_offset + 50])
                entity_type_data["max_spawn_count"] = int.from_bytes(
                    file[data_offset + 52 : data_offset + 54], "little", signed=True
                )
                entity_type_data["spawn_interval"] = int.from_bytes(
                    file[data_offset + 54 : data_offset + 56], "little", signed=True
                )
                entity_type_data["spawn_delay"] = int.from_bytes(
                    file[data_offset + 56 : data_offset + 58], "little", signed=True
                )
                entity_type_data["notify_entity_id"] = int.from_bytes(
                    file[data_offset + 58 : data_offset + 60], "little", signed=True
                )
                entity_type_data["collected_message"] = int.from_bytes(
                    file[data_offset + 60 : data_offset + 64], "little", signed=True
                )
                entity_type_data["collected_message_param1"] = int.from_bytes(
                    file[data_offset + 64 : data_offset + 68], "little", signed=True
                )
                entity_type_data["collected_message_param2"] = int.from_bytes(
                    file[data_offset + 68 : data_offset + 72], "little", signed=True
                )
            # Teleporter
            if entity_type == 14:
                target_position = {
                    "x": int.from_bytes(file[data_offset + 63 : data_offset + 67], "little", signed=True) / 4096.0,
                    "y": int.from_bytes(file[data_offset + 67 : data_offset + 71], "little", signed=True) / 4096.0,
                    "z": int.from_bytes(file[data_offset + 71 : data_offset + 74], "little", signed=True) / 4096.0,
                }

                entity_type_data["load_index"] = file[data_offset + 40]
                entity_type_data["target_index"] = file[data_offset + 41]
                entity_type_data["artifact_id"] = file[data_offset + 42]
                entity_type_data["active"] = bool(file[data_offset + 43])
                entity_type_data["invisible"] = bool(file[data_offset + 44])
                entity_type_data["entity_filename"] = (
                    str(file[data_offset + 44 : data_offset + 59], "utf-8").strip("\u0000").replace("\u0001", " ")
                )
                entity_type_data["target_position"] = target_position
                entity_type_data["node_name"] = str(file[data_offset + 74 : data_offset + 90], "utf-8").strip("\u0000")
            # Artifact
            if entity_type == 17:
                entity_type_data["model_id"] = file[data_offset + 40]
                entity_type_data["artifact_id"] = file[data_offset + 41]
                entity_type_data["active"] = bool(file[data_offset + 42])
                entity_type_data["has_base"] = bool(file[data_offset + 43])
                entity_type_data["message1_target"] = int.from_bytes(
                    file[data_offset + 44 : data_offset + 46], "little", signed=True
                )
                entity_type_data["message1"] = int.from_bytes(file[data_offset + 48 : data_offset + 52], "little")
                entity_type_data["message2_target"] = int.from_bytes(
                    file[data_offset + 52 : data_offset + 54], "little", signed=True
                )
                entity_type_data["message2"] = int.from_bytes(file[data_offset + 56 : data_offset + 60], "little")
                entity_type_data["message3_target"] = int.from_bytes(
                    file[data_offset + 60 : data_offset + 62], "little", signed=True
                )
                entity_type_data["message3"] = int.from_bytes(file[data_offset + 64 : data_offset + 68], "little")
            # Force Field
            if entity_type == 19:
                type = file[data_offset + 40]
                # if type == 9:
                #     continue

                width = {
                    "x": int.from_bytes(file[data_offset + 42 : data_offset + 46], "little", signed=True) / 4096.0,
                    "y": int.from_bytes(file[data_offset + 46 : data_offset + 50], "little", signed=True) / 4096.0,
                    "z": int.from_bytes(file[data_offset + 50 : data_offset + 54], "little", signed=True) / 4096.0,
                }

                height = {
                    "x": int.from_bytes(file[data_offset + 58 : data_offset + 62], "little", signed=True) / 4096.0,
                    "y": int.from_bytes(file[data_offset + 66 : data_offset + 70], "little", signed=True) / 4096.0,
                    "z": int.from_bytes(file[data_offset + 74 : data_offset + 78], "little", signed=True) / 4096.0,
                }

                entity_type_data["type"] = type
                entity_type_data["width"] = width
                entity_type_data["height"] = height
                entity_type_data["active"] = bool(file[data_offset + 78])

            entity_dict[i] = {
                "entity_type": entity_type,
                "entity_id": entity_id,
                "position": position,
                "up_vector": up_vector,
                "facing_vector": facing_vector,
                "entity_type_data": entity_type_data,
            }

            entry_start += entry_length
            entry_end += entry_length

        data_dict: dict = {"num_entities": num_entities, "entities": entity_dict}
        name = entity_file[16:-8]
        if name[4] == "1":
            entities_per_area["Alinos"][name] = data_dict
        elif name[4] == "2":
            entities_per_area["Celestial Archives"][name] = data_dict
        elif name[4] == "3":
            entities_per_area["Vesper Defense Outpost"][name] = data_dict
        elif name[4] == "4":
            entities_per_area["Arcterra"][name] = data_dict
        else:
            entities_per_area["Oubliette"][name] = data_dict

    with Path.open(export_path / "entity_data.json", "w") as f:
        json.dump(entities_per_area, f, indent=4)

    return entities_per_area


def main() -> None:
    export_path = Path(__file__).parent.joinpath("rdv_export")
    export_path.mkdir(parents=True, exist_ok=True)

    rom_path = "D:/Gaming/Modding/Games/Metroid Prime Hunters/Metroid Prime - Hunters (USA) (Rev 1).nds"
    rom = NintendoDSRom.fromFile(rom_path)
    entity_data = get_entity_data(rom, export_path)

    pickup_index = 0
    area_dict: dict = {}
    for area, all_data in entity_data.items():
        area_dict["name"] = area
        area_dict["extra"] = {}
        room_dict: dict = {}
        for room, room_data in all_data.items():
            door_index = 0
            teleporter_index = 0
            force_field_index = 0
            for room_id, area_name, room_name, ent_file in room_name_to_entity_file:
                if room == ent_file:
                    room = room_name  # noqa: PLW2901
                    room_dict[room] = {
                        "default_node": "Player Spawn",
                        "hint_features": [],
                        "extra": {
                            "room_id": room_id,
                            "entity_file": f"{ent_file}_Ent.bin",
                        },
                        "nodes": {},
                    }
                    break

            for entity_index, data in room_data["entities"].items():
                # Player Spawn
                if data["entity_type"] == 2:
                    room_dict[room]["nodes"]["Player Spawn"] = {
                        "node_type": "generic",
                        "heal": False,
                        "coordinates": data["position"],
                        "description": "",
                        "layers": ["default"],
                        "extra": {
                            "entity_id": data["entity_id"],
                            "up_vector": data["up_vector"],
                            "facing_vector": data["facing_vector"],
                            "entity_type_data": data["entity_type_data"],
                        },
                        "valid_starting_location": False,
                        "connections": {},
                    }
                # Door
                if data["entity_type"] == 3:
                    room_dict[room]["nodes"][f"Door {door_index}"] = {
                        "node_type": "dock",
                        "heal": False,
                        "coordinates": data["position"],
                        "description": "",
                        "layers": [
                            "default",
                        ],
                        "extra": {
                            "entity_id": data["entity_id"],
                            "up_vector": data["up_vector"],
                            "facing_vector": data["facing_vector"],
                            "entity_type_data": data["entity_type_data"],
                        },
                        "valid_starting_location": False,
                        "dock_type": "Door",
                        "default_connection": {
                            "region": None,
                            "area": None,
                            "node": None,
                        },
                        "default_dock_weakness": "Normal",
                        "exclude_from_dock_rando": False,
                        "incompatible_dock_weaknesses": [],
                        "override_default_open_requirement": None,
                        "override_default_lock_requirement": None,
                        "ui_custom_name": None,
                        "connections": {},
                    }
                    door_index += 1
                # Item Spawn
                if data["entity_type"] == 4 and data["entity_type_data"]["item_type"] not in (
                    [0, 1, 2, 12, 13, 14, 15, 16, 19]
                ):
                    room_dict[room]["nodes"][f"Pickup ({pickup_index})"] = {
                        "node_type": "pickup",
                        "heal": False,
                        "coordinates": data["position"],
                        "description": "",
                        "layers": ["default"],
                        "extra": {
                            "entity_id": data["entity_id"],
                            "up_vector": data["up_vector"],
                            "facing_vector": data["facing_vector"],
                            "entity_type_data": data["entity_type_data"],
                        },
                        "valid_starting_location": False,
                        "pickup_index": pickup_index,
                        "location_category": "minor",
                        "hint_features": [],
                        "connections": {},
                    }
                    pickup_index += 1
                # Teleporter
                if data["entity_type"] == 14:
                    room_dict[room]["nodes"][f"Teleporter {teleporter_index}"] = {
                        "node_type": "dock",
                        "heal": False,
                        "coordinates": data["position"],
                        "description": "",
                        "layers": ["default"],
                        "extra": {
                            "entity_id": data["entity_id"],
                            "up_vector": data["up_vector"],
                            "facing_vector": data["facing_vector"],
                            "entity_type_data": data["entity_type_data"],
                        },
                        "valid_starting_location": False,
                        "dock_type": "Other",
                        "default_connection": {
                            "region": None,
                            "area": None,
                            "node": None,
                        },
                        "default_dock_weakness": "Not Determined",
                        "exclude_from_dock_rando": False,
                        "incompatible_dock_weaknesses": [],
                        "override_default_open_requirement": None,
                        "override_default_lock_requirement": None,
                        "ui_custom_name": None,
                        "connections": {},
                    }
                    teleporter_index += 1
                # Artifact
                if data["entity_type"] == 17:
                    room_dict[room]["nodes"][f"Pickup ({pickup_index})"] = {
                        "node_type": "pickup",
                        "heal": False,
                        "coordinates": data["position"],
                        "description": "",
                        "layers": ["default"],
                        "extra": {
                            "entity_id": data["entity_id"],
                            "up_vector": data["up_vector"],
                            "facing_vector": data["facing_vector"],
                            "entity_type_data": data["entity_type_data"],
                        },
                        "valid_starting_location": False,
                        "pickup_index": pickup_index,
                        "location_category": "major",
                        "hint_features": [],
                        "connections": {},
                    }
                    pickup_index += 1
                # Force Field
                if data["entity_type"] == 19 and data["entity_type_data"]["type"] != 9:
                    room_dict[room]["nodes"][f"Force Field {teleporter_index}"] = {
                        "node_type": "configurable_node",
                        "heal": False,
                        "coordinates": data["position"],
                        "description": "",
                        "layers": ["default"],
                        "extra": {
                            "entity_id": data["entity_id"],
                            "up_vector": data["up_vector"],
                            "facing_vector": data["facing_vector"],
                            "entity_type_data": data["entity_type_data"],
                        },
                        "valid_starting_location": False,
                        "connections": {},
                    }
                    force_field_index += 1

        area_dict["areas"] = room_dict

        with Path.open(export_path / f"{area}.json", "w") as f:
            json.dump(area_dict, f, indent=4)


if __name__ == "__main__":
    main()
