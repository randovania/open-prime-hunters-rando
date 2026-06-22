import enum

from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.logger import LOG


class SuitColor(enum.Enum):
    DEFAULT = 0
    PURPLE = 1
    BLUE = 2
    BLACK = 3
    ORANGE = 4
    GREEN = 5


def patch_suit_color(rom: NintendoDSRom, suit_color: int) -> None:
    # Only modify the color if it not default
    new_color = SuitColor(suit_color)
    if new_color == SuitColor.DEFAULT:
        return

    LOG.info("Changing suit color")

    # Mapping of suit color to file names
    suit_color_mapping = {
        SuitColor.DEFAULT: ["01", "01"],
        SuitColor.PURPLE: ["02", "02"],
        SuitColor.BLUE: ["03", "03"],
        SuitColor.BLACK: ["04", "04"],
        SuitColor.ORANGE: ["team01", "Team01"],
        SuitColor.GREEN: ["team02", "Team02"],
    }

    # Default files to replace
    default_samus_tex_path = "models/Samus_pal_01_Tex.bin"
    default_gun_model_path = "models/SamusGun_img_01_Model.bin"
    default_gun_tex_path = "models/SamusGun_img_01_Tex.bin"

    # Get the model files associated with the new color
    new_samus_tex = rom.getFileByName(f"models/Samus_pal_{suit_color_mapping[new_color][0]}_Tex.bin")
    new_gun_model = rom.getFileByName(f"models/SamusGun_img_{suit_color_mapping[new_color][1]}_Model.bin")
    new_gun_tex = rom.getFileByName(f"models/SamusGun_img_{suit_color_mapping[new_color][1]}_Tex.bin")

    # Replace the bytes of the default models with the bytes of the new color
    rom.setFileByName(default_samus_tex_path, new_samus_tex)
    rom.setFileByName(default_gun_tex_path, new_gun_tex)
    rom.setFileByName(default_gun_model_path, new_gun_model)
