from src.graphics.Sprite import Sprite
from src.globals.UC import *

class Sprites:
    """
    Holds sprites for use in game
    """
    rory_battle1 = Sprite(
        200, 400, 320, 320,
        UC.main_char_image_01,
        (64, 177, 64),
    )
    emoji_chill = Sprite(
        200, 400, 200, 200,
        "../assets/images/test_images/Emoji-Chill.png",
        (64, 177, 64),
    )

    emoji_on_fire = Sprite(
        200, 400, 200, 200,
        "../assets/images/test_images/Emoji-On-Fire.png",
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