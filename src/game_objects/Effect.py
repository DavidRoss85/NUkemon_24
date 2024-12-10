import math
from src.globals.UC import UC
from src.graphics.Sprite import Sprite


class Effect:
    """
    Special effects objects that draw at the top layer of the screen. These are animated so their "frames"
    attribute is a list of sprites to cycle through
    (Effects are essentially a list of Sprite objects that draw to its own Sprite to give the illusion
    of animation. These are drawn over the battle screen for things like explosions etc.)
    """
    def __init__(self,x,y,width,height,frames=[]):
        self.__x=x  #x coord
        self.__y=y  #y coord
        self.__width=width  #width
        self.__height=height    #height
        self.__visible=True #toggle visibility
        self.__frames=frames #List of surfaces
        self.__frame_index=0    #current animation frame
        self.__max_frames=len(self.__frames)    #gets max frames in list

        #Main surface sprite of object
        self.__sprite=Sprite(self.__x,self.__y,self.__width,self.__height,None,(0,0,0),(127,127,127))

    def get_visible(self):
        """
        Return visibility
        """
        return self.__visible

    def get_x(self):
        """
        :return: x coord
        """
        return self.__x

    def get_y(self):
        """
        :return: y coord
        """
        return self.__y

    def set_visible(self, value: bool):
        """
        Toggle visibility
        :param value: Boolean (True/False)
        """
        self.__visible = value

    def set_x(self, x):
        """
        Set x coord
        :param x: x coord
        """
        self.__x = x

    def set_y(self, y):
        """
        Set y coord
        :param y: y coord
        """
        self.__y = y

    def __paint_effect_frame(self):
        """
        Uses the frame index to draw the appropriate sprite animation frame
        """

        index=self.__frame_index    #Get frame index
        if len(self.__frames)>0:    #Ensure there are frames in the list
            if index> len(self.__frames)-1: #Don't exceed max frames
                index=len(self.__frames)-1
            frame=self.__frames[self.__frame_index] #get the current frame sprite

            #Clear the current surface:
            self.__sprite.restore()
            #Draw the current frame:
            self.__sprite.draw_on_surface(
                frame.get_surface(),
                frame.get_surface().get_rect().x,
                frame.get_surface().get_rect().y
            )

    def set_frame_index(self,num):
        """
        Set the current animation frame
        :param num: Frame number
        """
        self.__frame_index= 0 if num>len(self.__frames)-1 else num

    def get_max_frames(self):
        """
        :return: total number of frames in list
        """
        return self.__max_frames

    def get_frame_index(self):
        """
        :return: Current frame index
        """
        return self.__frame_index

    def get_sprite(self):
        """
        Paints the current frame and returns the resulting sprite
        :return: Effect sprite for drawing
        """
        self.__paint_effect_frame()
        return self.__sprite

    def add_frame(self,sprite:Sprite):
        """
        Add a frame to the animation list
        :param sprite: Sprite object to add to the frame list
        """
        self.__frames.append(sprite)
        self.__max_frames=len(self.__frames)

    def add_multiple_frames(self,sprites:list):
        """
        Append a list of sprites to the frame list
        :param sprites: List of Sprite objects
        """
        self.__frames+=sprites
        self.__max_frames=len(self.__frames)

    #==================================================================================================================
    @staticmethod
    def generate_effect_array(image, width, height, new_width, new_height, stretch: bool = False, mask=(64, 177, 64)):
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
        sprite_list = []  # Stores the sprite frames

        # Retrieves the total size of the image
        big_picture = Sprite(0, 0, 0, 0, image, mask, (0, 0, 0), False)

        # Cycle through each section and crop image. Store to list:
        # Cycle through heights:
        for h in range(0, big_picture.get_height(), height):
            if big_picture.get_height() < h + height: break

            # Cycle through widths:
            for w in range(0, big_picture.get_width(), width):
                if big_picture.get_width() < w + width: break

                # Generate new sprite to copy image to (Used for stretching image)
                new_sprite = Sprite(0, 0, new_width, new_height, None, (0, 0, 0), (127, 127, 127))

                # Set up a cropped surface to blit big pic to
                cropped_image = Sprite(0, 0, width, height, None, (0, 0, 0), (127, 127, 127))
                # Blit big picture onto cropped surface:
                cropped_image.draw_on_surface(
                    big_picture.get_surface(),
                    -w, -h
                )

                # Stretch image onto new surface:
                new_sprite.draw_on_surface(
                    cropped_image.get_surface(),
                    0, 0, stretch
                )
                # add to list:
                sprite_list.append(new_sprite)

        # Return list
        return sprite_list

    # ==================================================================================================================
    @staticmethod
    def generate_battle_transition(old_surface, w, h):
        sprite_list = []  # Stores the sprite frames
        surface_width = UC.screen_width
        surface_height = UC.screen_height
        w_div = w
        h_div = h

        unit_width = math.ceil(surface_width / w_div)
        unit_height = math.ceil(surface_height / h_div)

        big_picture = Sprite(0, 0, surface_width, surface_height, None, (0, 0, 0), (127, 127, 127))
        big_picture.draw_on_surface(old_surface, 0, 0, True)

        for left in range(0, surface_width, unit_width):
            right = left + unit_width
            if left > surface_width:
                break
            for top in range(0, surface_height, unit_height):
                bottom = top + unit_height
                if top > surface_height:
                    break

                square_block = Sprite(0, 0, unit_width, unit_height, None, (1, 0, 0), (0, 0, 0))
                big_picture.draw_on_surface(square_block.get_surface(), left, top)

                new_surface = Sprite(0, 0, surface_width, surface_height, None, (0, 0, 0))
                new_surface.draw_on_surface(big_picture.get_surface(), 0, 0, True)

                sprite_list.append(new_surface)

        return sprite_list
