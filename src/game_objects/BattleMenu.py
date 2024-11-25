import pygame

from src.globals.UC import UC
from src.graphics.Sprite import Sprite

MASK = UC.image_mask_color

class BattleMenu:

    DEFAULT_PIC = UC.menu_box_image
    DEFAULT_FONT = UC.default_font
    DEFAULT_FONT_SIZE = UC.default_font_size
    DEFAULT_FONT_COLOR = UC.default_font_color
    DEFAULT_SELECTED_COLOR= UC.default_menu_item_selected_color
    DEFAULT_TEXT_TO_PIXEL_SCALE_WIDTH = 10
    DEFAULT_TEXT_TO_PIXEL_SCALE_HEIGHT = 5
    DEFAULT_TEXT_START_PERCENT_X = 8
    DEFAULT_TEXT_END_PERCENT_X = (100 - (DEFAULT_TEXT_START_PERCENT_X * 2)) / 100

    def __init__(self,x,y,width,height,menu_list:list=[],box_color:tuple=(0,0,0),mask:tuple=MASK):
        self.__x=x
        self.__y=y
        self.width=width
        self.height=height
        self.menu_list=menu_list
        self.color=box_color
        self.mask_color=mask
        self.__visible=True
        self.__current_selection=0
        self.__background_pic=BattleMenu.DEFAULT_PIC
        self.__font=BattleMenu.DEFAULT_FONT
        self.__font_size = BattleMenu.DEFAULT_FONT_SIZE
        self.__font_color = BattleMenu.DEFAULT_FONT_COLOR
        self.__font_color_selected=BattleMenu.DEFAULT_SELECTED_COLOR
        self.__text_pixel_scale_width = BattleMenu.DEFAULT_TEXT_TO_PIXEL_SCALE_WIDTH
        self.__text_pixel_scale_height = BattleMenu.DEFAULT_TEXT_TO_PIXEL_SCALE_HEIGHT
        self.__text_start_percent_x = BattleMenu.DEFAULT_TEXT_START_PERCENT_X
        self.__text_end_percent_x = BattleMenu.DEFAULT_TEXT_END_PERCENT_X

        self.__sprite=Sprite(x,y,width,height,self.__background_pic,self.mask_color,self.color)
        self.display_menu()

    def set_visible(self,value:bool=True):
        self.__visible=value

    def set_current_selection(self,selection):
        self.__current_selection=selection
        self.display_menu()

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_visible(self):
        return self.__visible

    def get_current_selection(self):
        return self.menu_list[self.__current_selection]

    def get_sprite(self):
        return self.__sprite

    def next_menu_item(self):
        if self.__current_selection < len(self.menu_list) - 1:
            self.__current_selection+=1
            self.display_menu()

    def prev_menu_item(self):
        if self.__current_selection>0:
            self.__current_selection-=1
            self.display_menu()

    def display_menu(self):
        """
        Displays all menu items
        :return:
        """
        self.clear_menu()
        for i,item in enumerate(self.menu_list):
            m_item="> "+ item if i==self.__current_selection else item
            m_color= self.__font_color_selected if i==self.__current_selection else self.__font_color
            font_surface= self.write_line(m_item, m_color)
            rect=font_surface.get_rect()
            # Set the x location of the text based on width of box
            rect.x = int(self.width * self.__text_start_percent_x / 100)
            # Set the text line based on the line number and size of box
            rect.y = self.height // self.__text_pixel_scale_height * i + 1
            self.__sprite.draw_on_surface(font_surface, rect.x, rect.y)

    def update_menu(self,new_menu):
        self.menu_list=new_menu
        self.display_menu()

    def clear_menu(self):
        """
        Clears current text in the menu.
        :return:
        """
        #Completely restores the box to its original form
        self.__sprite.restore()
    def write_line(self,text,color):
        """
        Takes a string of text and creates a pygame compatible surface to render
        :param color:
        :param text: Text to write
        :return: pygame surface
        """
        font = pygame.font.Font(self.__font, size=self.__font_size)
        font.bold = True
        font_surface = font.render(text, False, color)

        return font_surface