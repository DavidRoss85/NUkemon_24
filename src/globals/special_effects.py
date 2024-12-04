from src.globals.sprites import Sprites
from src.graphics.Effect import Effect
from src.graphics.Sprite import Sprite
from src.globals.UC import *
from src.utils.utils import generate_effect_array




class SpecialEffects:

    punches= Effect(0, 0, 250, 250, generate_effect_array(
        UC.punch_effect_image,
        250, 250,250,250
    ))

    discreet_math= Effect(0, 0, 600, 600, generate_effect_array(
        UC.discreet_math_effect_image,
        250, 250,600,600,True,(255,255,255)
    ))



# xxx=generate_effect_array("../assets/images/backgrounds/Background8.png",100,100)