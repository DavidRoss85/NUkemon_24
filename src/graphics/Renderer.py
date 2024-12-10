from src.globals.UC import UC
BACKCOLOR=UC.game_back_color
WIDTH=UC.screen_width
HEIGHT=UC.screen_height

import pygame


class Renderer:
    """
    Handles all drawing of Sprites and surfaces to the pygame engine
    """
    def __init__(self, screen_width=WIDTH, screen_height=HEIGHT, back_color=BACKCOLOR):

        self.__layers=[[], [], [],[],[]]    #List of layers (Nested lists)
        self.__main_surface=pygame.Surface((screen_width,screen_height))    #Pygame's main surface to draw on
        self.__back_color=back_color    #The default back color of the screen
        self.__main_surface.fill(self.__back_color) #Fill the main surface with the default back color
        self.__rect=self.__main_surface.get_rect()  #Dimensions of the main surface
        self.__screen=pygame.display.set_mode((screen_width,screen_height)) #Set pygame screen mode
        pygame.init()   #initialize pygame

    def clear_all_layers(self):
        """
        Clear all layers
        """
        self.__layers=[[], [], [],[],[]]

    def add_to_layer(self,item,layer=0):
        """
        Add an item to a specific layer
        :param item: Game object containing a sprite to render
        :param layer: Layer index to store to
        """
        self.__layers[layer].append(item)

    def __render_surface(self,sprite,location):
        """
        Render a sprite's "surface" to the main pygame "surface"
        :param sprite: Pygame sprite
        :param location: rect object containing coords, width and height
        """
        self.__main_surface.blit(sprite.get_surface(), location)

    def render_all(self):
        """
        Each layer is a list of items to render.
        Items will be rendered according to which layer they are in
        Top most layers are rendered last
        """
        #Add loops to render all layers in order

        #Clear surface
        self.__main_surface.fill(self.__back_color)

        #Draw all layers on surface
        for layer in self.__layers:
            for item in layer:
                if item.get_visible():  #Only draw if visibility is toggled on
                    sprite=item.get_sprite()
                    rect=sprite.get_rect()
                    rect.x=item.get_x()
                    rect.y=item.get_y()
                    self.__render_surface(sprite,rect)

        #Copy main surface to screen
        self.__screen.blit(self.__main_surface,self.__rect)

    def get_screen_surface(self):
        """
        Returns the last thing shown as a surface. Used for transitions
        :returns: Pygame surface
        """
        return self.__screen

    def flip_screen(self):
        """
        Performs a pygame "flip" where the screen is updated with the main surface
        """
        pygame.display.flip()

