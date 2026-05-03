from open_prime_hunters_rando.patching.asm import GenerateArmBytes, bitfield_to_bytes, read_bytes_from_file


class AsmPatches:
    def __init__(self, configuration: dict) -> None:
        # Setup
        self.starting_items = configuration["starting_items"]
        self.game_patches = configuration["game_patches"]
        self.ammo_sizes = configuration["ammo_sizes"]
        self.validate_bitfields()

        # Starting Items
        self.starting_ammo = patch_starting_ammo(self.starting_items["ammo"])
        self.starting_energy = patch_starting_energy(self.starting_items["energy"])
        self.starting_missiles = patch_starting_missiles(self.starting_items["missiles"])
        self.starting_octoliths = bitfield_to_bytes(self.starting_items["octoliths"])
        self.starting_weapons = bitfield_to_bytes(self.starting_items["weapons"])

        # Ammo Sizes
        self.ammo_per_expansion = patch_ammo_per_expansion(self.ammo_sizes["ua_expansion"])
        self.missile_launcher = patch_missile_launcher(self.ammo_sizes["missile_launcher"])
        self.missiles_per_expansion = patch_ammo_per_expansion(self.ammo_sizes["missile_expansion"])

        # Game Patches
        self.unlock_planets = unlock_planets(self.game_patches["unlock_planets"])

    def validate_bitfields(self) -> None:
        bitfields = ["weapons", "octoliths"]
        # Validate weapons and octoliths bitfields
        for bitfield in bitfields:
            if len(self.starting_items[bitfield]) != 8:
                raise ValueError(
                    f"Invalid starting {bitfield} bitfield. Must contain 8 numbers, got "
                    f" {len(self.starting_items[bitfield])}!"
                )

            for bitflag in self.starting_items[bitfield]:
                if bitflag not in ["0", "1"]:
                    raise ValueError(f"Invalid starting {bitfield} bitfield. Must only contain 0 or 1, got {bitflag}!")


def unlock_planets(unlock_planets: dict) -> bytes:
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

    return bitfield_to_bytes(planets)


def patch_starting_energy(starting_energy: int) -> bytes:
    return starting_energy.to_bytes(4, "little")


def patch_missile_launcher(ammo_value: int) -> bytes:
    binary = read_bytes_from_file("missile_launcher.bin")
    new_instructions = GenerateArmBytes(ammo_value).add(2, 2)
    modified_bytes = binary.replace(b"\x32\x20\x82\xe2", new_instructions)

    return modified_bytes


def patch_ammo_per_expansion(ammo_value: int) -> bytes:
    binary = read_bytes_from_file("ammo_per_expansion.bin")
    new_instructions = GenerateArmBytes(ammo_value).add(2, 2)
    modified_bytes = binary.replace(b"\xff\x20\x82\xe2", new_instructions)

    return modified_bytes


def patch_starting_missiles(ammo_value: int) -> bytes:
    binary = read_bytes_from_file("starting_ammo.bin")
    new_instructions = GenerateArmBytes(ammo_value).mov(8)
    modified_bytes = binary.replace(b"2\x80\xa0\xe3", new_instructions)

    return modified_bytes


def patch_starting_ammo(ammo_value: int) -> bytes:
    binary = read_bytes_from_file("starting_ammo.bin")
    new_instructions = GenerateArmBytes(ammo_value).mov(2)
    modified_bytes = binary.replace(b"2\x80\xa0\xe3", new_instructions)

    return modified_bytes
