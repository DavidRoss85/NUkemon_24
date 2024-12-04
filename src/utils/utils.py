import os
from src.graphics.Sprite import Sprite

def merge_dictionaries(dictionary1, dictionary2):
    my_dict = dictionary1.copy()
    for key, value in dictionary2.items():
        if key in my_dict and isinstance(my_dict[key], dict) and isinstance(value, dict):
            my_dict[key] = merge_dictionaries(my_dict[key], value)
        else:
            my_dict[key] = value
    return my_dict

def generate_effect_array(image, width, height,new_width,new_height,stretch:bool=False,mask=(64,177,64)):
    """
    Takes an image and splits it into an array of smaller images to use for animation frames
    :param image:
    :param width:
    :param height:
    :param new_width:
    :param new_height:
    :param stretch:
    :param mask:
    :return:
    """
    sprite_list = []    #Stores the sprite frames

    #Retrieves the total size of the image
    big_picture = Sprite(0, 0, 0, 0, image, mask, (0,0,0), False)

    #Cycle through each section and crop image. Store to list:
    #Cycle through heights:
    for h in range(0,big_picture.get_height(),height):
        if big_picture.get_height()<h+height: break

        #Cycle through widths:
        for w in range(0,big_picture.get_width(),width):
            if big_picture.get_width()<w+width:break

            #Generate new sprite to copy image to (Used for stretching image)
            new_sprite=Sprite(0,0,new_width,new_height,None,(0,0,0),(127,127,127))

            #Set up a cropped surface to blit big pic to
            cropped_image=Sprite(0,0,width,height,None,(0,0,0),(127,127,127))
            #Blit big picture onto cropped surface:
            cropped_image.draw_on_surface(
                big_picture.get_surface(),
                -w,-h
            )

            #Stretch image onto new surface:
            new_sprite.draw_on_surface(
                cropped_image.get_surface(),
                0,0,stretch
            )
            #add to list:
            sprite_list.append(new_sprite)

    #Return list
    return sprite_list


def count_lines_in_project(directory):
    """
    Tool to count lines of code across project
    :param directory: root directory
    :return: Integer (Total number of lines across all files)
    """
    total_lines=0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path= os.path.join(root,file)
                with open(file_path, 'r',encoding='utf-8') as f:
                    lines = f.readlines()
                    total_lines += len(lines)

    return total_lines