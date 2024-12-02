import pygame

from src.globals.UC import UC
from src.graphics.Sprite import Sprite

MASK = UC.image_mask_color

class BattleMenu:
    """
    User menu interface during battles
    This object uses a dictionary where the keys represent the choices the user sees.
    The values can be other dictionaries (Sub menus) or functions which are executed
    when the user confirms their selection
    """
    #Static:
    DEFAULT_PIC = UC.menu_box_image #Default image
    DEFAULT_FONT = UC.default_font  #Default font
    DEFAULT_FONT_SIZE = UC.default_font_size    #Default font size
    DEFAULT_FONT_COLOR = UC.default_font_color  #Default font color
    DEFAULT_SELECTED_COLOR= UC.default_menu_item_selected_color #Default selected menu color
    DEFAULT_TEXT_TO_PIXEL_SCALE_WIDTH = 10  #Used for text placement
    DEFAULT_TEXT_TO_PIXEL_SCALE_HEIGHT = UC.default_font_pixel_height   #Used for text placement
    DEFAULT_TEXT_START_PERCENT_X = 8    #Used for text placement
    DEFAULT_TEXT_END_PERCENT_X = (100 - (DEFAULT_TEXT_START_PERCENT_X * 2)) / 100   #Used for text placement

    def __init__(self,x,y,width,height,menu_dictionary:dict={},box_color:tuple=(0,0,0),mask:tuple=MASK):
        """
        Constructor
        :param x: x coord
        :param y: y coord
        :param width: width
        :param height: height
        :param menu_dictionary: Dictionary with menu items and commands
        :param box_color: hue/color of the box (R,G,B) tuple
        :param mask: mask for sprite (R,G,B) tuple
        """
        self.__x=x  #x coord
        self.__y=y  #y coord
        self.__width=width  #width
        self.__height=height    #height
        self.__menu_dictionary=menu_dictionary  #dictionary of commands
        self.__color=box_color  #color (R,G,B) tuple
        self.__mask_color=mask  #transparent color (R,G,B) tuple
        self.__max_items=5  #Maximum items before scrolling takes over
        self.__visible=True #Hidden/Shown
        self.__current_selection_number=0   #Index of current selection
        self.__current_selection="" #Title of current selection (Used for dictionary reference)

        self.__background_pic=BattleMenu.DEFAULT_PIC    #Picture of the box
        self.__font=BattleMenu.DEFAULT_FONT #Font
        self.__font_size = BattleMenu.DEFAULT_FONT_SIZE #Font size
        self.__font_color = BattleMenu.DEFAULT_FONT_COLOR   #Font color
        self.__font_color_selected=BattleMenu.DEFAULT_SELECTED_COLOR    #Selected color
        self.__text_pixel_scale_width = BattleMenu.DEFAULT_TEXT_TO_PIXEL_SCALE_WIDTH    #Controls width of font sprite
        self.__text_pixel_scale_height = BattleMenu.DEFAULT_TEXT_TO_PIXEL_SCALE_HEIGHT  #controls height of font sprite
        self.__text_start_percent_x = BattleMenu.DEFAULT_TEXT_START_PERCENT_X   #Where to begin drawing text
        self.__text_end_percent_x = BattleMenu.DEFAULT_TEXT_END_PERCENT_X   #Where to end drawing text

        #Generate sprite:
        self.__sprite=Sprite(x, y, width, height, self.__background_pic, self.__mask_color, self.__color)

        #Show menu items:
        self.display_menu()

    def set_max_items(self,num):
        """
        Set max number of line items in menu
        :param num: number of lines
        :return:
        """
        self.__max_items=num

    def set_visible(self,value:bool=True):
        """
        Set visibility
        :param value: True/False
        :return:
        """
        self.__visible=value

    def set_current_selection_number(self,number):
        """
        Set current selection index
        :param number: index
        :return:
        """
        self.__current_selection_number=number
        self.display_menu()

    def set_x(self,x):
        """
        Set x coord
        :param x: Integer
        :return:
        """
        self.__x=x

    def set_y(self,y):
        """
        Set y coord
        :param y: Integer
        :return:
        """
        self.__y=y

    def set_position(self,x,y):
        """
        Set position x and y coords
        :param x: x coord (Integer)
        :param y: y coord (Integer)
        :return:
        """
        self.set_x(x)
        self.set_y(y)

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
        :return: visibility (True/False)
        """
        return self.__visible

    def get_current_selection(self):
        """
        Returns current menu selection in dictionary form
        :return: (Dictionary)
        """
        return self.__menu_dictionary[self.__current_selection]

    def get_sprite(self):
        """
        Returns menu sprite (Used in rendering)
        :return: Sprite
        """
        return self.__sprite

    def next_menu_item(self):
        """
        Go to the next menu item
        :return:
        """
        if self.__current_selection_number < len(self.__menu_dictionary) - 1:
            self.__current_selection_number+=1
            self.display_menu()

    def prev_menu_item(self):
        """
        Go to the previous menu item
        :return:
        """
        if self.__current_selection_number>0:
            self.__current_selection_number-=1
            self.display_menu()

    def display_menu(self):
        """
        Displays all menu items
        :return:
        """
        #Set sprite in case parameters changed:
        self.__sprite = Sprite(self.__x, self.__y, self.__width, self.__height, self.__background_pic, self.__mask_color, self.__color)
        #Refresh:
        self.clear_menu()

        selection_list=[]   #Holds a list of menu options to display
        n=0 #Counter for hiding menu that exceed max number

        #For each item in dictionary
        for i,item in enumerate(self.__menu_dictionary):
            #If the user scrolls down to half the menu it will begin to scroll thereafter.
            #Only displays specified number of items depending on current user selection.
            if i<self.__current_selection_number-(self.__max_items//2): continue #Don't show indexes too low
            if n>self.__max_items-1:break   #Don't exceed max

            #Append to the list of items to show:
            selection_list.append(item)

            m_color = self.__font_color    #modify font color

            #if current selection is this item add an arrow in front and update color:
            if i == self.__current_selection_number:
                self.__current_selection=item
                item="> "+ item
                m_color=self.__font_color_selected

            #Generate font surface and get dimensions:
            font_surface= self.write_line(item, m_color)
            rect=font_surface.get_rect()

            # Set the x location of the text based on __width of box
            rect.x = int(self.__width * self.__text_start_percent_x / 100)

            # Set the text line based on the line number and size of box
            rect.y = self.__text_pixel_scale_height * n + 1

            #Draw text onto sprite:
            self.__sprite.draw_on_surface(font_surface, rect.x, rect.y)

            #increment for count
            n += 1

    def update_menu(self,new_menu,width=None,height=None):
        """
        Change menu items and update dictionaries and size
        :param new_menu: (Dictionary)
        :param width: width
        :param height:
        :return:
        """
        #update dictionaries:
        self.__menu_dictionary=new_menu
        if self.__current_selection_number> len(self.__menu_dictionary)-1:
            self.__current_selection_number=0

        #Verify width and height are specified before updating
        if width is not None:
            self.__width=width
        if height is not None:
            self.__height=height

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