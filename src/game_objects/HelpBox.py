import pygame
from src.globals.UC import UC
from src.graphics.Sprite import Sprite

MASK=UC.image_mask_color

class HelpBox:
    DEFAULT_PIC = UC.stat_box_image
    DEFAULT_FONT = UC.default_font
    DEFAULT_FONT_SIZE = int(UC.default_font_size/1.5)
    DEFAULT_FONT_COLOR = UC.default_font_color


    def __init__(self,x,y,width,height,color:tuple=(0,0,0),mask:tuple=MASK):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__color = color
        self.__visible=True

        self.__background_pic=self.DEFAULT_PIC
        self.__font = self.DEFAULT_FONT
        self.__font_size = self.DEFAULT_FONT_SIZE
        self.__font_color = self.DEFAULT_FONT_COLOR
        self.__text_start_x = 35
        self.__text_start_y = 5

        self.__sprite = Sprite(x, y, width, height, self.__background_pic, mask, color)
        self.clear_self()

    def set_visible(self, value: bool = True):
        self.__visible = value

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_visible(self):
        return self.__visible

    def get_sprite(self):
        return self.__sprite


    def clear_self(self):
        """
        Clears current text in box.
        :return:
        """
        # Completely restores the box to its original form
        self.__sprite.restore()

    def write_in_box(self,text):
        self.clear_self()
        info_text=self.write_text(text)
        self.__sprite.draw_on_surface(info_text, self.__text_start_x, self.__text_start_y)

    def write_text(self,text,font_style=None,font_size=None):
        """
        Takes a string of text and creates a pygame compatible surface to render
        :param text: Text to write
        :param font_style: define font. Default if None
        :param font_size: define size of font. Default if None
        :return: pygame surface
        """
        font_style=self.__font if font_style is None else font_style
        font_size = self.__font_size if font_size is None else font_size

        font = pygame.font.Font(font_style, size=font_size)
        font.bold = True
        font_surface = font.render(text, False, self.__font_color)

        return font_surface