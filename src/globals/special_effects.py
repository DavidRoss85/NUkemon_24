from src.game_objects.Effect import Effect
from src.globals.UC import *

class SpecialEffects:
    """
    Special effect objects are generated and stored here
    """

    punches= Effect(0, 0, 250, 250, Effect.generate_effect_array(
        UC.punch_effect_image,
        250, 250,250,250
    ))

    sleep = Effect(0, 0, 250, 250, Effect.generate_effect_array(
        UC.sleep_effect_image,
        250, 250, 250, 250,False,(255,255,255)
    ))
    confused = Effect(0, 0, 250, 250, Effect.generate_effect_array(
        UC.confused_effect_image,
        250, 250, 250, 250,False,(255,255,255)
    ))

    discreet_math= Effect(0, 0, 600, 600, Effect.generate_effect_array(
        UC.discreet_math_effect_image,
        250, 250,600,600,True,(255,255,255)
    ))

    algorithms = Effect(0, 600, 600, 600, Effect.generate_effect_array(
        UC.alorithms_effect_image,
        250, 250, 600, 600, True, (255, 255, 255)
    ))

    big_o = Effect(0, 600, 600, 600, Effect.generate_effect_array(
        UC.big_o_effect_image,
        250, 250, 600, 600, True, (255, 255, 255)
    ))
# xxx=generate_effect_array("../assets/images/backgrounds/Background8.png",100,100)