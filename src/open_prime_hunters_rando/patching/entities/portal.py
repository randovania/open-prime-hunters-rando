from typing import TypedDict

from open_prime_hunters_rando.parsing.formats.entities.entity_file import EntityFile
from open_prime_hunters_rando.parsing.formats.entities.entity_types.object import Object, ObjectEffectFlags, ObjectFlags
from open_prime_hunters_rando.parsing.formats.entities.entity_types.teleporter import Teleporter
from open_prime_hunters_rando.parsing.level_data import ALL_AREAS, ALL_PORTAL_FILE_NAMES


class PortalProperties(TypedDict):
    entity_id: int
    target_index: int
    active: bool
    entity_file_name: str


def patch_portals(entity_file: EntityFile, portals: list[PortalProperties], room_name: str) -> None:
    if room_name == "Docking Bay":
        _fix_incubation_vault_03_portal_spawn(entity_file)

    for portal in portals:
        _patch_portal_destination(entity_file, portal, room_name)


def _patch_portal_destination(entity_file: EntityFile, portal: PortalProperties, room_name: str) -> None:
    entity_id = portal["entity_id"]
    file_name = portal["entity_file_name"]

    entity = entity_file.get_entity(entity_id, Teleporter)

    # target_index is the load_index of the desination portal
    entity.target_index = portal["target_index"]

    if file_name not in ALL_PORTAL_FILE_NAMES:
        raise ValueError(f"Invalid entity file_name for portal entity {entity_id} in {room_name}: {file_name}")
    file_name = f"{file_name}.bin"
    file_name = file_name[:15]

    entity.entity_file_name = file_name

    # Only change the active field if a value is provided
    is_active = portal.get("active", None)
    if is_active is not None:
        entity.active = is_active

    # Add a scan point above the portal that indicates the destination room
    # No return portals are invisible and do not get a scan point since they aren't usable
    # Magma Drop entrance portal is invisible but does get a scan point since it is usable
    if (room_name == "High Ground" and entity_id == 57) or not entity.invisible:
        # The first custom string id for portal scans is 475
        scan_id = 475
        for area_data in ALL_AREAS:
            for room, level_data in area_data.items():
                assert level_data.portal_file_name is not None
                if level_data.portal_file_name in file_name:
                    scan_id += level_data.room_id - 27
                    break

        destination_scan = Object.create(
            node_name=entity.node_name,
            layer_state=entity.layer_state,
            position=entity.position,
            object_flags=ObjectFlags.STATE_BIT0,
            object_effect_flags=ObjectEffectFlags.UNKNOWN,
            model_id=0,
            scan_id=scan_id,
            effect_interval=10,
            effect_on_inverals=1,
        )
        destination_scan.position.y += 2
        entity_file.append_entity(destination_scan)


def _fix_incubation_vault_03_portal_spawn(incubation_vault_03: EntityFile) -> None:
    # The portal from Docking Bay to Incubation Vault 03 spawned Samus at the room spawn and not at the portal
    portal = incubation_vault_03.get_entity(7, Teleporter)
    portal.target_index = 27
