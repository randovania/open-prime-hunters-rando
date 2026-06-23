import enum

from ndspy.rom import NintendoDSRom

from open_prime_hunters_rando.logger import LOG


class SuitColor(enum.Enum):
    VARIA = "varia"
    PURPLE = "purple"
    BLUE = "blue"
    BLACK = "black"
    ORANGE = "orange"
    GREEN = "green"


def patch_suit_color(rom: NintendoDSRom, suit_color: str) -> None:
    # Only modify the color if it not varia
    new_color = SuitColor(suit_color)
    if new_color == SuitColor.VARIA:
        return

    LOG.info("Changing suit color")

    # Mapping of suit color to file names
    suit_color_mapping = {
        SuitColor.VARIA: ["01", "01"],
        SuitColor.PURPLE: ["02", "02"],
        SuitColor.BLUE: ["03", "03"],
        SuitColor.BLACK: ["04", "04"],
        SuitColor.ORANGE: ["team01", "Team01"],
        SuitColor.GREEN: ["team02", "Team02"],
    }

    # File paths for textures and models of varia Samus and gun
    varia_samus_tex_path = "models/Samus_pal_01_Tex.bin"
    varia_gun_model_path = "models/SamusGun_img_01_Model.bin"
    varia_gun_tex_path = "models/SamusGun_img_01_Tex.bin"

    # Get the model files associated with the new color
    new_samus_tex = rom.getFileByName(f"models/Samus_pal_{suit_color_mapping[new_color][0]}_Tex.bin")
    new_gun_model = rom.getFileByName(f"models/SamusGun_img_{suit_color_mapping[new_color][1]}_Model.bin")
    new_gun_tex = rom.getFileByName(f"models/SamusGun_img_{suit_color_mapping[new_color][1]}_Tex.bin")

    # Replace the bytes of the varia models with the bytes of the new color
    rom.setFileByName(varia_samus_tex_path, new_samus_tex)
    rom.setFileByName(varia_gun_tex_path, new_gun_tex)
    rom.setFileByName(varia_gun_model_path, new_gun_model)
