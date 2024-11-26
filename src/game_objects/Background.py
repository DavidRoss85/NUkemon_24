from src.graphics.Sprite import Sprite
from src.globals.UC import UC

MASK = UC.image_mask_color


class Background:

    DEFAULT_BACKGROUND=UC.background_image
    def __init__(self,x,y,width,height,image=None,mask:tuple=MASK,tint:tuple=(0,0,0)):
        self.__x=x
        self.__y=y
        self.__width=width
        self.__height=height
        self.__visible=True
        if image is None:
            self.__background_pic=Background.DEFAULT_BACKGROUND
        else:
            self.__background_pic=image
        self.__mask=mask
        self.__tint=tint
        self.__sprite = Sprite(x, y, self.__width, self.__height, self.__background_pic, mask, tint)
        self.clear_self()


    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_visible(self):
        return self.__visible

    def get_sprite(self):
        return self.__sprite

    def clear_self(self):
        self.__sprite.restore()

    def set_visible(self,value):
        self.__visible=value

    def set_background(self,image):
        self.__background_pic=image
        self.__sprite = Sprite(self.__x, self.__y, self.__width, self.__height, self.__background_pic, self.__mask, self.__tint)

    def set_tint(self,tint:tuple=(0,0,0)):
        self.__tint=tint
        self.__sprite = Sprite(self.__x, self.__y, self.__width, self.__height, self.__background_pic, self.__mask,
                               self.__tint)
