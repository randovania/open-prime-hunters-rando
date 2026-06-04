from typing import TypedDict

from open_prime_hunters_rando.parsing.formats.entities.entity_file import EntityFile
from open_prime_hunters_rando.parsing.formats.entities.entity_types.teleporter import Teleporter
from open_prime_hunters_rando.parsing.level_data import ALL_PORTAL_FILE_NAMES


class PortalProperties(TypedDict):
    entity_id: int
    target_index: int
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


def _fix_incubation_vault_03_portal_spawn(incubation_vault_03: EntityFile) -> None:
    # The portal from Docking Bay to Incubation Vault 03 spawned Samus at the room spawn and not at the portal
    portal = incubation_vault_03.get_entity(7, Teleporter)
    portal.target_index = 27
