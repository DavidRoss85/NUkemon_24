from src.globals.sprites import Sprites
from src.graphics.Effect import Effect
from src.graphics.Sprite import Sprite


def generate_effect_array(image, width, height,new_width,new_height,mask=(64,177,64)):
    sprite_list = []
    big_picture = Sprite(0, 0, 0, 0, image, (0, 0, 0), None, False)
    for h in range(0,big_picture.get_height(),height):
        if big_picture.get_height()<h+height: break
        for w in range(0,big_picture.get_width(),width):
            if big_picture.get_width()<w+width:break
            new_sprite=Sprite(0,0,new_width,new_height,None,(0,0,0),(127,127,127))
            cropped_image=Sprite(0,0,0,0,image,mask,(0,0,0),False)
            new_sprite.draw_on_surface(
                cropped_image.get_surface(),
                -w,-h,True
            )
            sprite_list.append(new_sprite)

    return sprite_list


class SpecialEffects:

    punches= Effect(0, 0, 250, 250, generate_effect_array(
        "../assets/images/effects/punches_effect.bmp",
        250, 250,250,250
    ))

    discreet_math= Effect(0, 0, 600, 600, generate_effect_array(
        "../assets/images/effects/discreet_math_effect.bmp",
        250, 250,600,600,(255,255,255)
    ))



# xxx=generate_effect_array("../assets/images/backgrounds/Background8.png",100,100)