from src.graphics.Sprite import Sprite

class Sprites:
    """
    Holds sprites for use in game
    """
    rory_battle1 = Sprite(
        200, 400, 300, 300,
        "../assets/images/test_images/Boy_backpack1_hmmm_bk.png",
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
        "../assets/images/characters/Male_Professor_1_transparent.png",
        (64,177,64),
    )

    professor_b= Sprite(
        200,400,350,350,
        "../assets/images/characters/Male_Professor_2_transparent.png",
        (64, 177, 64),
    )

    teaching_assistant_a = Sprite(
        200,400,350,350,
        "../assets/images/characters/Female_TA1_transparent.png",
        (64,177,64)
    )