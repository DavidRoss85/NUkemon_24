from src.graphics.Sprite import Sprite
from src.globals.UC import *

class Sprites:
    """
    Sprites a constructed and stored here:
    """
    male_normal_backpack_behind = Sprite(
        200, 400, 450, 450,
        UC.male_normal_behind_image,
        (64, 177, 64),
    )

    male_muscular_shirtless_behind= Sprite(
        200, 400, 550, 550,
        UC.male_muscle_behind_image,
        (64, 177, 64),
    )

    girl_brown_hair = Sprite(
        200, 400, 550, 550,
        UC.female_brown_hair_image,
        (64, 177, 64),
    )

    girl_black_hair = Sprite(
        200, 400, 550, 550,
        UC.female_black_hair_image,
        (64, 177, 64),
    )

    emoji_chill = Sprite(
        200, 400, 200, 200,
        f"{UC.absolute_path}/assets/images/test_images/Emoji-Chill.png",
        (64, 177, 64),
    )

    emoji_on_fire = Sprite(
        200, 400, 200, 200,
        f"{UC.absolute_path}/assets/images/test_images/Emoji-On-Fire.png",
        (64, 177, 64),
    )

    professor_a= Sprite(
        200,400,275,275,
        UC.professor_a_image_01,
        (64,177,64),
    )

    professor_b= Sprite(
        200,400,350,350,
        UC.professor_b_image_01,
        (64, 177, 64),
    )

    teaching_assistant_a = Sprite(
        200,400,350,350,
        UC.t_a_image_01,
        (64,177,64)
    )

    nu_husky=Sprite(
        200,400,350,350,
        UC.nu_husky_image_01,
    )