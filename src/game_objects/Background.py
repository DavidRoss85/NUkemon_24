from src.graphics.Sprite import Sprite
from src.globals.UC import UC

MASK = UC.image_mask_color


class Background:
    """
    This object handles loading the background. Default background is a global constant
    """
    #Static
    DEFAULT_BACKGROUND=UC.background_image  #Default background image

    def __init__(self,x,y,width,height,image=None,mask:tuple=MASK,tint:tuple=(0,0,0)):
        self.__x=x  #x coordinate
        self.__y=y  #y coordinate
        self.__width=width  #width
        self.__height=height    #height
        self.__visible=True #hidden/shown

        #Use default image if none specified:
        if image is None:
            self.__background_pic=Background.DEFAULT_BACKGROUND
        else:
            self.__background_pic=image

        self.__mask=mask    #Transparent color
        self.__tint=tint    #Change hue of background (Additive blending)

        #Generate the background sprite:
        self.__sprite = Sprite(x, y, self.__width, self.__height, self.__background_pic, mask, tint)

        #Refresh the  background after generating
        self.clear_self()


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

    def get_visible(self):
        """
        :return: visibility status
        """
        return self.__visible

    def get_sprite(self):
        """
        Returns the sprite object of the background (Used for rendering)
        :return: Sprite
        """
        return self.__sprite

    def clear_self(self):
        """
        Restores background to the way it was when it was first loaded
        :return:
        """
        self.__sprite.restore()

    def set_visible(self,value):
        """
        Set visibility
        :param value: True/False
        :return:
        """
        self.__visible=value

    def set_background(self,image):
        """
        Change background image
        :param image: (String) Image file path
        :return:
        """
        self.__background_pic=image
        self.__sprite = Sprite(self.__x, self.__y, self.__width, self.__height, self.__background_pic, self.__mask, self.__tint)

    def set_tint(self,tint:tuple=(0,0,0)):
        """
        Change hue/color of background (Additive blend)
        :param tint: (R,G,B) tuple
        :return:
        """
        self.__tint=tint
        self.__sprite = Sprite(self.__x, self.__y, self.__width, self.__height, self.__background_pic, self.__mask,
                               self.__tint)
