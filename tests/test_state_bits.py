from open_prime_hunters_rando.patching.entities.shield_key_patches import create_shield_key_messages
from open_prime_hunters_rando.patching.entities.state_bits import (
    ShieldKeyData,
    UnlockMessage,
    get_state_bit,
)


def test_get_state_bit():
    shield_key_data = get_state_bit(49)

    assert shield_key_data == ShieldKeyData(
        area_name="Vesper Defense Outpost",
        room_name="Fuel Stack",
        entity_id=57,
        unlock_message=UnlockMessage.SHIELD,
    )


def test_create_shield_key_messages():
    all_messages = create_shield_key_messages()

    assert all_messages == [
        "PSHIELD KEY FOUND\\a DOOR was unlocked in ALINOS - ECHO HALL!",
        "PSHIELD KEY FOUND\\an ARTIFACT SHIELD was deactivated in ALINOS - ELDER PASSAGE!",
        "PSHIELD KEY FOUND\\an ARTIFACT SHIELD was deactivated in ALINOS - HIGH GROUND!",
        "PSHIELD KEY FOUND\\an ARTIFACT SHIELD was deactivated in ALINOS - CRASH SITE!",
        "PSHIELD KEY FOUND\\a FORCE FIELD was disabled in ALINOS - COUNCIL CHAMBER!",
        "PSHIELD KEY FOUND\\an ARTIFACT SHIELD was deactivated in ALINOS - PISTON CAVE!",
        "PSHIELD KEY FOUND\\an ARTIFACT SHIELD was deactivated in CELESTIAL ARCHIVES - DATA SHRINE 01!",
        "PSHIELD KEY FOUND\\a DOOR was unlocked in CELESTIAL ARCHIVES - DATA SHRINE 03!",
        "PSHIELD KEY FOUND\\an ARTIFACT SHIELD was deactivated in CELESTIAL ARCHIVES - SYNERGY CORE!",
        "PSHIELD KEY FOUND\\an ARTIFACT SHIELD was deactivated in CELESTIAL ARCHIVES - DOCKING BAY!",
        "PSHIELD KEY FOUND\\an ARTIFACT SHIELD was deactivated in CELESTIAL ARCHIVES - INCUBATION VAULT 01!",
        "PSHIELD KEY FOUND\\an ARTIFACT SHIELD was deactivated in CELESTIAL ARCHIVES - NEW ARRIVAL REGISTRATION!",
        "PSHIELD KEY FOUND\\a FORCE FIELD was disabled in VESPER DEFENSE OUTPOST - COMPRESSION CHAMBER!",
        "PSHIELD KEY FOUND\\a FORCE FIELD was disabled in VESPER DEFENSE OUTPOST - WEAPONS COMPLEX!",
        "PSHIELD KEY FOUND\\an ARTIFACT SHIELD was deactivated in VESPER DEFENSE OUTPOST - WEAPONS COMPLEX!",
        "PSHIELD KEY FOUND\\an ARTIFACT SHIELD was deactivated in VESPER DEFENSE OUTPOST - STASIS BUNKER!",
        "PSHIELD KEY FOUND\\an ARTIFACT SHIELD was deactivated in VESPER DEFENSE OUTPOST - STASIS BUNKER!",
        "PSHIELD KEY FOUND\\an ARTIFACT SHIELD was deactivated in VESPER DEFENSE OUTPOST - FUEL STACK!",
        "PSHIELD KEY FOUND\\a DOOR was unlocked in ARCTERRA - SIC TRANSIT!",
        "PSHIELD KEY FOUND\\a FORCE FIELD was disabled in ARCTERRA - ICE HIVE!",
        "PSHIELD KEY FOUND\\a DOOR was unlocked in ARCTERRA - FROST LABYRINTH!",
        "PSHIELD KEY FOUND\\a FORCE FIELD was disabled in ARCTERRA - FAULT LINE!",
        "PSHIELD KEY FOUND\\an ARTIFACT SHIELD was deactivated in ARCTERRA - SANCTORUS!",
        "PSHIELD KEY FOUND\\an ARTIFACT SHIELD was deactivated in ARCTERRA - SUBTERRANEAN!",
    ]
