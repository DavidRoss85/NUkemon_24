import os

import pygame


#Holds Universal Constants
class UC:
    """
    Universal constants (Game settings)
    """
    absolute_path=os.path.join(os.path.dirname(__file__),'..')
    screen_width=1024   #Screen width
    screen_height=768   #Screen height
    image_mask_color=(64,177,64)    #Mask color for sprites (R,G,B) tuple
    game_back_color=(0,0,0) #Background color (R,G,B) tuple
    MUSIC_EVENT_END= pygame.USEREVENT + 13
    music_repeat_point=MUSIC_EVENT_END

#Image assets:
    image_path=f"{absolute_path}/assets/images/"
    background_image=f"{image_path}/backgrounds/Background8.png"
    info_box_image=f"{image_path}text_box.png"
    menu_box_image = f"{image_path}text_box.png"
    stat_box_image=f"{image_path}stat_box.png"

    #Characters:
    character_path=f"{absolute_path}/assets/images/characters/"
    male_normal_behind_image= f"{character_path}Boy_backpack4.png"
    male_muscle_behind_image=f"{character_path}Muscle_boy_backpack.png"
    female_brown_hair_image=f"{character_path}Girl_brown_hair.png"
    female_black_hair_image=f"{character_path}Girl_black_hair.png"
    professor_a_image_01= f"{character_path}Male_Professor_1_transparent.png"
    professor_b_image_01= f"{character_path}Male_Professor_2_transparent.png"
    t_a_image_01=f"{character_path}Female_TA1_transparent.png"
    nu_husky_image_01=f"{character_path}NU_Husky_transparent.png"

    #Special Effects:
    punch_effect_image=f"{absolute_path}/assets/images/effects/punches_effect.bmp"
    discreet_math_effect_image=f"{absolute_path}/assets/images/effects/discreet_math_effect.bmp"

 #Default Font settings:
    default_font= f"{absolute_path}/assets/fonts/Grand9K_Pixel.ttf"
    default_font_size=24    #Size
    default_font_color="black"  #Color
    default_font_pixel_height=40    #How much pixel height to reserve for fonts

#Game menu:
    default_menu_item_selected_color = "blue"   #Selected text color

#Sound dictionary:
    sound_path= f"{absolute_path}/assets/sounds/"
    music_path= f"{sound_path}/music/"
    se_path=f"{sound_path}/effects/"
    animator_sound_dictionary={
        "punch": "punch-classic-betacut.mp3",
        "base_boom": "slow-motion-glitch-rewind-joshua-chivers.mp3",
        "swish": "swish-airy-swish-smartsound.mp3",
        "boop": "boop.wav"
    }
    music_file=f"rivalry-sulyya4.ogg"
# Music from #Uppbeat
# https://uppbeat.io/t/sulyya/rivalry
# License code: BTSQ70TOAU4SG7RB

# Sound Effects from Mixkit
# https://mixkit.co/free-sound-effects/click/
# Sound Effects under free license can be used in video games 
# for commercial and non-commercial projects