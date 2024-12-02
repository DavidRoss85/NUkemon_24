import pygame

from src.globals.UC import UC
from src.graphics.Sprite import Sprite


MASK = UC.image_mask_color

class InfoBox:
    """
    Scrolling text box
    """
    #Static constants
    DEFAULT_PIC = UC.info_box_image
    DEFAULT_FONT = UC.default_font
    DEFAULT_FONT_SIZE = UC.default_font_size
    DEFAULT_FONT_COLOR = UC.default_font_color
    DEFAULT_TEXT_TO_PIXEL_SCALE_WIDTH = 15
    DEFAULT_TEXT_TO_PIXEL_SCALE_HEIGHT=5
    DEFAULT_TEXT_START_PERCENT_X = 8
    DEFAULT_TEXT_END_PERCENT_X= (100 - (DEFAULT_TEXT_START_PERCENT_X*2)) / 100

    def __init__(self,x,y,box_width,box_height,box_text,n_lines:int=4,box_color:tuple=(0,0,0),mask:tuple=MASK):
        self.__x=x
        self.__y=y
        self.__width=box_width
        self.__height=box_height
        self.__text=box_text
        self.__color=box_color
        self.__n_text_lines=n_lines
        self.__visible=True
        self.__background_pic = InfoBox.DEFAULT_PIC
        self.__font=InfoBox.DEFAULT_FONT
        self.__font_size=InfoBox.DEFAULT_FONT_SIZE
        self.__font_color=InfoBox.DEFAULT_FONT_COLOR
        self.__text_pixel_scale_width=InfoBox.DEFAULT_TEXT_TO_PIXEL_SCALE_WIDTH
        self.__text_pixel_scale_height=InfoBox.DEFAULT_TEXT_TO_PIXEL_SCALE_HEIGHT
        self.__text_start_percent_x=InfoBox.DEFAULT_TEXT_START_PERCENT_X
        self.__text_end_percent_x=InfoBox.DEFAULT_TEXT_END_PERCENT_X

        self.__sprite=Sprite(x, y, box_width, box_height, self.__background_pic, mask, box_color)
        self.write_text(self.__text)

    def set_visible(self,value:bool=True):
        self.__visible=value

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_visible(self):
        return self.__visible

    def get_sprite(self):
        return self.__sprite

    def write_text(self,text):
        """
        Takes a string of text and writes it into the box. It will push earlier text out of the box
        :param text: Text string to format
        :return:
        """
        #Split the text into lines that fit into the box dimensions:
        lines=self.__fit_text_in_box(text)
        #Clear any existing text in the box:
        self.clear_text()
        #For each line of text:
        for i,line in enumerate(lines):
            #Generate new font surface with text
            font_surface=self.write_line(line)
            #Get the bounding rect for the text surface (Used for positioning)
            rect = font_surface.get_rect()
            #Set the x location of the text based on __width of box
            rect.x = int(self.__width * self.__text_start_percent_x/100)
            #Set the text line based on the line number and size of box
            rect.y = self.__height // self.__text_pixel_scale_height * i + 1
            #Set the total __width of the surface to a percent of the __width
            rect.width = int(self.__width * self.__text_end_percent_x)
            #Create a surface that will crop out any accidental over extended text (blend the __color to something other than text __color)
            fitted_surface=Sprite(0, 0, rect.width, rect.height, None, (0, 0, 0),(64,177,64))
            #Draw the text onto that surface
            fitted_surface.get_surface().blit(font_surface, (0, 0, rect.width, rect.height)) #This is a Sprite
            #Place text in the appropriate place in the box:
            self.__sprite.draw_on_surface(fitted_surface.get_surface(), rect.x, rect.y)

    def clear_text(self):
        """
        Clears current text in box.
        :return:
        """
        #Completely restores the box to its original form
        self.__sprite.restore()

    def __fit_text_in_box(self,text:str):
        """
        Takes a string of text and separates into a list of lines of text that fit in window
        :param text: Text to format
        :return: List containing lines of text
        """
        word_list = text.split(" ")
        line_list=[]
        #Set number of lines in list:
        for _ in range(self.__n_text_lines):
            line_list.append("")

        max_len=self.__width//self.__text_pixel_scale_width #Num characters to allow to match __width of box (This is an approximation)
        total_length=0
        line_words=""
        new_line=False
        for word in word_list:
            if len(line_words) > 0 and line_words[-1] == "\n":
                new_line=True
            #Add length of previous string with new word:
            total_length+=len(word)
            #Check if new length will exceed space requirements:
            if total_length < max_len and not new_line:
                #If it fits then append the new word to the old string:
                line_words=f"{line_words} {word}"
                #Add 1 to length to account for space character:
                total_length+=1
            else:
                #If the new word will not fit:
                #Check the length of the old string to see if it's empty:
                if len(line_words)==0:
                    #If empty then just add it to the string anyway:
                    line_words=word
                else:
                    #Otherwise push the old text into the bottom and start a new line of text with the new word
                    line_list.pop(0)
                    line_words=line_words.rstrip("\n")
                    line_list.append(line_words)
                    line_words=word
                    total_length=len(word)
                new_line=False

        #After all text has been evaluated, if there is still text left over, push it into last line:
        if len(line_words)>0:
            if line_words[-1]=="\n":
                line_words=line_words.rstrip("\n")
                line_list.append(line_words)
                line_list.append("")
                line_list.pop(0)
                line_list.pop(0)
            else:
                line_list.append(line_words)
                line_list.pop(0)

        #Return list containing lines of text
        return line_list

    def write_line(self,text):
        """
        Takes a string of text and creates a pygame compatible surface to render
        :param text: Text to write
        :return: pygame surface
        """
        font = pygame.font.Font(self.__font, size=self.__font_size)
        font.bold = True
        font_surface = font.render(text, False, self.__font_color)

        return font_surface

