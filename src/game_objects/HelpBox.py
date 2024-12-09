import pygame
from src.globals.UC import UC
from src.graphics.Sprite import Sprite

MASK=UC.image_mask_color

class HelpBox:
    """
    This is a text box that appears at the top of the window to help players understand
    the menu selection items and what the character skills do
    """

    #Create defaults from Universal Constant (UC) class
    DEFAULT_PIC = UC.stat_box_image
    DEFAULT_FONT = UC.default_font
    DEFAULT_FONT_SIZE = int(UC.default_font_size/1.5)
    DEFAULT_FONT_COLOR = UC.default_font_color


    def __init__(self,x,y,width,height,color:tuple=(0,0,0),mask:tuple=MASK):
        self.__x = x    #x coord
        self.__y = y    #y coord
        self.__width = width    #width
        self.__height = height  #height
        self.__color = color    #This color additively blends with the sprite
        self.__visible=True #Toggle visibility

        self.__background_pic=self.DEFAULT_PIC  #Background pic
        self.__font = self.DEFAULT_FONT #Font
        self.__font_size = self.DEFAULT_FONT_SIZE   #Font size
        self.__font_color = self.DEFAULT_FONT_COLOR #Font color
        self.__text_start_x_percent = int(self.__width*.05) #Start x coord of the text drawing
        self.__text_start_y = 5 #Start y coord for text drawing

        #Main sprite for rendering
        self.__sprite = Sprite(x, y, width, height, self.__background_pic, mask, color)
        self.clear_self()

    def set_visible(self, value: bool = True):
        """
        Toggle visibility
        :param value: Boolean (True/False)
        """
        self.__visible = value

    def get_x(self):
        """
        :returns: x coord
        """
        return self.__x

    def get_y(self):
        """
        :returns: y coord
        """
        return self.__y

    def get_visible(self):
        """
        :returns: visibility
        """
        return self.__visible

    def get_sprite(self):
        """
        :returns: Object Sprite
        """
        return self.__sprite


    def clear_self(self):
        """
        Clears current text in box.
        :return:
        """
        # Completely restores the box to its original form
        self.__sprite.restore()

    def write_in_box(self,text):
        """
        Renders the text to the sprite object
        :param text: String to render
        """
        self.clear_self()
        info_text=self.write_text(text)
        self.__sprite.draw_on_surface(info_text, self.__text_start_x_percent, self.__text_start_y)

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