import pygame

from src.globals.UC import UC
from src.graphics.Sprite import Sprite

MASK=UC.image_mask_color
INFO_BOX_PIC=UC.info_box_image
FONT=UC.default_font
FONT_SIZE=UC.default_font_size
FONT_COLOR=UC.default_font_color

class InfoBox:
    def __init__(self,x,y,box_width,box_height,box_text,box_color:tuple=(0,0,0),mask:tuple=MASK):
        self.__x=x
        self.__y=y
        self.__width=box_width
        self.__height=box_height
        self.__text=box_text
        self.__color=box_color
        self.__sprite=Sprite(x, y, box_width, box_height, INFO_BOX_PIC, mask,box_color)
        self.write_text(self.__text)


    def write_text(self,text):
        self.clear_text()
        font=pygame.font.Font(FONT,size=FONT_SIZE)
        font.bold=True
        font_surface=font.render(text,False,FONT_COLOR)
        rect=font_surface.get_rect()
        rect.x=self.__width//10
        rect.y=self.__height//10
        rect.width=int(self.__width*.8)
        rect.height=int(self.__height*.8)
        self.__sprite.draw_on_surface(font_surface,rect.x,rect.y)

    def clear_text(self):
        self.__sprite.restore()

    def get_sprite(self):
        return self.__sprite
