#Holds Universal Constants
class UC:
    """
    Universal constants (Game settings)
    """
    screen_width=1024   #Screen width
    screen_height=768   #Screen height
    image_mask_color=(64,177,64)    #Mask color for sprites (R,G,B) tuple
    game_back_color=(0,0,0) #Background color (R,G,B) tuple

#Image assets:
    background_image="../assets/images/backgrounds/Background8.png"
    info_box_image="../assets/images/text_box.png"
    menu_box_image = "../assets/images/text_box.png"
    stat_box_image="../assets/images/stat_box.png"
    #Characters:
    main_char_image_01= "../assets/images/characters/Boy_backpack3.png"
    professor_a_image_01= "../assets/images/characters/Male_Professor_1_transparent.png"
    professor_b_image_01= "../assets/images/characters/Male_Professor_2_transparent.png"
    t_a_image_01="../assets/images/characters/Female_TA1_transparent.png"

 #Default Font settings:
    default_font= "../assets/fonts/Grand9K_Pixel.ttf"
    default_font_size=24    #Size
    default_font_color="black"  #Color
    default_font_pixel_height=40    #How much pixel height to reserve for fonts

#Game menu:
    default_menu_item_selected_color = "blue"   #Selected text color

