from open_prime_hunters_rando.patching.asm import (
    GenerateArmBytes,
    bitfield_to_bytes,
    create_bitmask,
    read_bytes_from_file,
)
from open_prime_hunters_rando.patching.game_version import DataSectionAddresses


class AsmPatches:
    def __init__(self, configuration: dict, data_section: DataSectionAddresses) -> None:
        # Setup
        self.starting_items = configuration["starting_items"]
        self.game_patches = configuration["game_patches"]
        self.ammo_sizes = configuration["ammo_sizes"]
        self.refill_sizes = configuration["refill_sizes"]

        # Starting Items
        self.starting_ammo = patch_starting_ammo(self.starting_items["ammo"])
        self.starting_energy = patch_starting_energy(self.starting_items["energy"])
        self.starting_missiles = patch_starting_missiles(self.starting_items["missiles"])
        self.starting_octoliths = bitfield_to_bytes(self.starting_items["octoliths"])
        self.starting_weapons = patch_starting_weapons(self.starting_items["weapons"])

        # Ammo Sizes
        self.ammo_per_expansion = patch_ammo_per_expansion(self.ammo_sizes["ua_expansion"])
        self.missile_launcher = patch_missile_launcher(
            self.ammo_sizes["missile_launcher"], data_section.story_save_data
        )
        self.missiles_per_expansion = patch_ammo_per_expansion(self.ammo_sizes["missile_expansion"])

        # Energy/Ammo Refills
        self.small_energy = patch_energy_refills(self.refill_sizes["small_energy"])
        self.medium_energy = patch_energy_refills(self.refill_sizes["medium_energy"])
        self.large_energy = patch_energy_refills(self.refill_sizes["large_energy"])
        self.small_ammo = patch_ammo_refills(self.refill_sizes["small_ammo"])
        self.large_ammo = patch_ammo_refills(self.refill_sizes["large_ammo"])
        self.refill_play_sfx = patch_refill_sound()

        # Game Patches
        self.init_save_file_rewrite = patch_planets_and_artifacts(
            self.game_patches["unlock_planets"], self.starting_items["artifacts"]
        )


def patch_starting_energy(starting_energy: int) -> bytes:
    return starting_energy.to_bytes(4, "little")


def patch_starting_weapons(starting_weapons: dict[str, bool]) -> bytes:
    weapons = [
        starting_weapons["shock_coil"],
        starting_weapons["magmaul"],
        starting_weapons["judicator"],
        starting_weapons["imperialist"],
        starting_weapons["battlehammer"],
        starting_weapons["missile_launcher"],
        starting_weapons["volt_driver"],
        True,  # Power Beam
    ]

    return bitfield_to_bytes(weapons)


def patch_missile_launcher(ammo_value: int, story_save_data_address: int) -> bytes:
    binary = read_bytes_from_file("missile_launcher.bin")
    new_instructions = GenerateArmBytes(ammo_value).add(1, 1)

    # Replace the StorySaveData address based on the version
    ssd = story_save_data_address.to_bytes(4, "little")
    modified_bytes = binary.replace(b"\x32\x10\x81\xe2", new_instructions).replace(b"P\x8c\x0e\x02", ssd)

    return modified_bytes


def patch_ammo_per_expansion(ammo_value: int) -> bytes:
    return GenerateArmBytes(ammo_value).add(2, 2)


def patch_starting_missiles(ammo_value: int) -> bytes:
    # The default instruction for starting missiles is mov r8, #0x32
    return GenerateArmBytes(ammo_value).mov(8)


def patch_starting_ammo(ammo_value: int) -> bytes:
    # The default instruction for starting ammo is mov r2, #0x19C
    return GenerateArmBytes(ammo_value).mov(2)


def patch_planets_and_artifacts(unlock_planets: dict, starting_artifacts: dict) -> bytes:
    binary = read_bytes_from_file("optimized_story_save_init.bin")

    # Starting Planets
    planets = [
        unlock_planets["Arcterra"],  # Arcterra 1
        unlock_planets["Arcterra"],  # Arcterra 2
        unlock_planets["Vesper Defense Outpost"],  # Vesper Defense Outpost 1
        unlock_planets["Vesper Defense Outpost"],  # Vesper Defense Outpost 2
        True,  # Celestial Archives 1 (Always unlocked)
        True,  # Celestial Archives 2 (Always unlocked)
        unlock_planets["Alinos"],  # Alinos 1
        unlock_planets["Alinos"],  # Alinos 2
    ]

    planets_instruction = bitfield_to_bytes(planets) + b"\x10\xa0\xe3"

    # Starting Artifacts (0-24)
    artifact_bitfields = ""

    for artifacts in reversed(starting_artifacts.values()):
        artifact_bitfields += artifacts

    artifact_bitmask = create_bitmask(artifact_bitfields)

    # Replace bytes from unlocked planets and starting artifacts
    modified_bytes = binary.replace(b"\x0c\x10\xa0\xe3", planets_instruction).replace(
        b"\xff\xff\xff\xff", artifact_bitmask
    )

    return modified_bytes


def patch_energy_refills(refill_value: int) -> bytes:
    return refill_value.to_bytes()


def patch_ammo_refills(refill_value: int) -> bytes:
    binary = read_bytes_from_file("ammo_refill.bin")
    converted_value = (refill_value * 10).to_bytes(4, "little")
    placeholder_value = b"\xff\x00\x00\x00"
    modified_bytes = binary.replace(placeholder_value, converted_value)

    return modified_bytes


def patch_refill_sound() -> bytes:
    """
    Overwrites the original instruction of loading from the sp to just moving a direct value
    This is necessary to preserve the sfx when picking up a small/large energy refill that has its values changed
    """
    return GenerateArmBytes(30, False).mov(0)
