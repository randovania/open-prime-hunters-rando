from typing import TypedDict

from open_prime_hunters_rando.parsing.formats.entities.entity_file import EntityFile
from open_prime_hunters_rando.parsing.formats.entities.entity_types.door import Door, DoorType
from open_prime_hunters_rando.parsing.formats.entities.enum import WeaponType


class DoorProperties(TypedDict):
    entity_id: int
    weapon_type: WeaponType
    locked: bool


def patch_doors(entity_file: EntityFile, doors: list[DoorProperties], room_name: str) -> None:
    if room_name == "Fault Line":
        _lock_fault_line_magmaul_door(entity_file)
    if room_name == "Sic Transit":
        _patch_sic_transit_inner_door(entity_file)

    for door in doors:
        _patch_door_weakness(entity_file, door, room_name)


def _patch_door_weakness(entity_file: EntityFile, door: DoorProperties, room_name: str) -> None:
    entity_id = door["entity_id"]
    weapon_type = WeaponType(door["weapon_type"])

    entity = entity_file.get_entity(entity_id, Door)

    # Break if trying to change weakness of Morph Ball or Boss doors
    if entity.door_type not in (DoorType.STANDARD, DoorType.THIN):
        raise ValueError(
            f"Unable to patch entity {entity_id} in {room_name}. Only Standard and Thin door types can be modified."
        )
    # If the new type is the same as the original type, skip changing it
    if weapon_type == entity.weapon_type:
        return

    # Change the weakness
    entity.weapon_type = weapon_type

    # Unlock doors that are changed to Power Beam
    if weapon_type == WeaponType.POWER_BEAM:
        entity.locked = False
    # Activate and lock doors changed to another weapon
    else:
        entity.locked = True


def _lock_fault_line_magmaul_door(fault_line: EntityFile) -> None:
    # The door from Sic Transit is a Magmaul door but not locked in game
    magmaul_door = fault_line.get_entity(31, Door)
    magmaul_door.locked = True


def _patch_sic_transit_inner_door(sic_transit: EntityFile) -> None:
    # The inner door is normally a standard door which looks bad and doesn't make sense
    inner_door = sic_transit.get_entity(24, Door)
    inner_door.door_type = DoorType.THIN
