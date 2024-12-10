import pygame

from src.globals.UC import UC
from src.graphics.Sprite import Sprite
from src.players.Player import Player

MASK = UC.image_mask_color

class StatBox:
    """
    Displays the __player or __enemy Name/Level/HP/MP etc
    The statbox starts with an image then procedurally draws other surfaces onto its
    sprite before passing off for rendering.
    HP/MP bars are red/green/blue square surfaces drawn over each other
    """
    #Static constants
    DEFAULT_PIC = UC.stat_box_image
    DEFAULT_FONT = UC.default_font
    DEFAULT_FONT_SIZE = UC.default_font_size
    DEFAULT_FONT_COLOR = UC.default_font_color
    DEFAULT_TEXT_TO_PIXEL_SCALE_WIDTH = 10
    DEFAULT_TEXT_TO_PIXEL_SCALE_HEIGHT=5
    DEFAULT_TEXT_START_PERCENT_X = 20
    DEFAULT_TEXT_END_PERCENT_X= (100 - (DEFAULT_TEXT_START_PERCENT_X*2)) / 100

    def __init__(self,linked_object,x,y,box_width,box_height,box_color:tuple=(0,0,0),mask:tuple=MASK):
        self.__x=x  #x coord
        self.__y=y  #y coord
        self.__width=box_width  #width
        self.__height=box_height    #height
        self.__color=box_color  #Additive blend color (Tuple)
        self.__linked_object:Player=linked_object   #Player or enemy object that feeds information

        #These are used for animation smoothness:
        #Displayed health and mana go up and down slowly, different from actual hp/mp
        self.__displayed_health=linked_object.get_current_character().get_curr_hp()
        self.__displayed_mana = linked_object.get_current_character().get_curr_mp()
        #Keeps an animation going even if other animation queues up:
        self.__animating_hp=False
        self.__animating_mp=False

        self.__visible=True #Toggle visibility

        self.__background_pic = StatBox.DEFAULT_PIC #Background pic
        self.__font=self.DEFAULT_FONT   #Font
        self.__font_size=self.DEFAULT_FONT_SIZE #Font size
        self.__font_color=self.DEFAULT_FONT_COLOR   #Font color
        self.__text_pixel_scale_width=self.DEFAULT_TEXT_TO_PIXEL_SCALE_WIDTH    #Text scaling width
        self.__text_start_percent_x=self.DEFAULT_TEXT_START_PERCENT_X   #Text start location
        self.__text_end_percent_x=self.DEFAULT_TEXT_END_PERCENT_X   #Text end location

        #Main sprite for rendering
        self.__sprite=Sprite(x, y, box_width, box_height, self.__background_pic, mask, box_color)
        self.update_stats()



    def set_visible(self,value:bool=True):
        """
        Toggle visibility
        :param value: Boolean (True/False)
        """
        self.__visible=value

    def get_animating(self):
        """
        Check the current animation status. Used for continuous hp/mp bar animations
        :return: True/False
        """
        if self.__animating_hp or self.__animating_mp:
            return True
        else:
            return False

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
        :return: visibility
        """
        return self.__visible

    def get_sprite(self):
        """
        :return: Object Sprite
        """
        return self.__sprite

    def display_name(self):
        """
        Shows the character name in the upper left corner of the box
        :return:
        """
        #Create text surface:
        font_surface=self.write_text(self.__linked_object.get_current_character().get_name())
        rect=font_surface.get_rect()

        #Surface that fits into box in case font surface is too wide
        fitted_surface = Sprite(0, 0, self.__width/2, rect.height, None, (0, 0, 0), (64, 177, 64))
        # Draw the text onto that surface
        fitted_surface.get_surface().blit(font_surface, (0, 0, rect.width, rect.height))  # This is a Sprite

        #Update main sprite
        self.__sprite.draw_on_surface(fitted_surface.get_surface(),self.__text_start_percent_x,5)

    def display_level(self):
        """
        Displays the level of the character in the upper right corner of the box
        :return:
        """
        #Create a text surface for the "Lv:" text (Smaller font)
        label_surface = self.write_text("Lv : ",None,self.__font_size//2)
        #Create a text surface for the actual level (Regular font)
        number_surface=self.write_text(str(self.__linked_object.get_current_character().get_level()))
        rect=number_surface.get_rect()

        # Surface that fits into box in case font surface is too wide
        fitted_surface = Sprite(0, 0, self.__width//1.5, rect.height, None, (0, 0, 0), (64, 177, 64))
        # Draw the text onto that surface
        fitted_surface.get_surface().blit(label_surface,label_surface.get_rect())
        fitted_surface.get_surface().blit(number_surface, (label_surface.get_rect().width+1, 0, rect.width, rect.height))  # This is a Sprite

        #update main Sprite
        self.__sprite.draw_on_surface(fitted_surface.get_surface(),self.__width//1.5+1,5)

    def display_health(self):
        """
        Displays the green health bar and text with max hp
        :return:
        """
        #Get current character
        curr_char=self.__linked_object.get_current_character()
        #Get max hp of current character
        max_hp=curr_char.get_max_hp()

        if max_hp==0: return #Prevent div by zero
        #How much to decrement the bar by for animations (1% of health or 1, whichever is larger)
        dec_amt=max(max_hp//100,1)
        #Get current hp level
        curr_hp=curr_char.get_curr_hp()

        #If current health dips below what is displayed, start animating the displayed health to decrease
        #__animating_hp/mp Tells battle system to keep animating during certain pauses of gameplay
        if curr_hp < self.__displayed_health <= max_hp:
            self.__displayed_health=self.__displayed_health-dec_amt
            self.__animating_hp=True
        else:
            self.__displayed_health=curr_hp
            self.__animating_hp=False

        #The size of the bar is controlled by this float: hp/max-hp
        health_fraction= self.__displayed_health/max_hp

        #The underlying red bar that shows max hp:
        health_bar_red=Sprite(self.__width//10,self.__height//2.5,self.__width//1.25,self.__height//10,None,(1,1,1),(255,0,0))
        rect_red=health_bar_red.get_rect()
        #Draw read bar onto sprite:
        self.__sprite.draw_on_surface(health_bar_red.get_surface(),rect_red.x,rect_red.y)

        # Calculate the width of the health bar:
        green_bar_width = max(int(rect_red.width * health_fraction), 1)

        #The overlaying green bar that shows current hp
        health_bar_green=Sprite(rect_red.x, rect_red.y, green_bar_width, rect_red.height, None, (1, 1, 1), (0, 255, 0))
        #Drawn the green bar on to sprite:
        self.__sprite.draw_on_surface(health_bar_green.get_surface(),rect_red.x,rect_red.y)

        #Write text representation for health
        health_text=self.write_text(f"{curr_hp}/{max_hp}",None,self.__font_size//2)
        #Draw text onto sprite
        self.__sprite.draw_on_surface(health_text, rect_red.x, rect_red.y+self.__height//10)

    def display_mana(self):
        """
        Displays the blue mana bar with text below the health bar
        :return:
        """
        #Get current character
        curr_char = self.__linked_object.get_current_character()
        #Get max mp of current character
        max_mp=curr_char.get_max_mp()

        if max_mp==0: return    #Prevent div by zero
        # How much to decrement the bar by for animations (1% of mana or 1, whichever is larger)
        dec_amt = max(max_mp // 100,1)
        #Get current mp of character
        curr_mp=curr_char.get_curr_mp()

        # If current mana dips below what is displayed, start animating the displayed bar to decrease
        # __animating_hp/mp Tells battle system to keep animating during certain pauses of gameplay
        if curr_mp < self.__displayed_mana<= max_mp:
            self.__displayed_mana=self.__displayed_mana-dec_amt
            self.__animating_mp=True
        else:
            self.__displayed_mana=curr_mp
            self.__animating_mp=False

        # The size of the bar is controlled by this float:mp/max-mp
        mana_fraction = curr_mp / max_mp

        # The underlying red bar that shows max mp:
        mana_bar_red = Sprite(self.__width // 2, self.__height // 2, self.__width // 2.5, self.__height // 20,
                              None, (1, 1, 1), (255,0, 0))
        rect_red = mana_bar_red.get_rect()
        #Draw red bar onto sprite
        self.__sprite.draw_on_surface(mana_bar_red.get_surface(), rect_red.x, rect_red.y)

        # Calculate the width of the mana bar:
        blue_bar_width = max(int(rect_red.width * mana_fraction), 1)

        #The overlying blue bar that shows current mp
        mana_bar_blue = Sprite(rect_red.x, rect_red.y, blue_bar_width, rect_red.height, None,
                               (1, 1, 1), (0, 0, 255))
        #Draw onto sprite
        self.__sprite.draw_on_surface(mana_bar_blue.get_surface(), rect_red.x, rect_red.y)

        #Mana text:
        mana_text = self.write_text(f"{curr_char.get_curr_mp()}/{curr_char.get_max_mp()}", None,
                                    self.__font_size // 2)
        #Draw mana text onto sprite
        self.__sprite.draw_on_surface(mana_text, rect_red.x, rect_red.y + self.__height // 20)

    def update_stats(self):
        """
        Refreshes all the displays in the box
        :return:
        """
        self.clear_self()
        self.display_name()
        self.display_level()
        self.display_health()
        self.display_mana()

    def clear_self(self):
        """
        Clears current text in box.
        :return:
        """
        # Completely restores the box to its original form
        self.__sprite.restore()

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

