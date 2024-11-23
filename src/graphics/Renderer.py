from src.globals.UC import UC
BACKCOLOR=UC.game_back_color
WIDTH=UC.screen_width
HEIGHT=UC.screen_height

import pygame


class Renderer:
    def __init__(self, screen_width=WIDTH, screen_height=HEIGHT, back_color=BACKCOLOR):
        self.__layers=[[], [], []]
        self.__main_surface=pygame.Surface((screen_width,screen_height))
        self.__back_color=back_color
        self.__main_surface.fill(self.__back_color)
        self.__rect=self.__main_surface.get_rect()
        self.__screen=pygame.display.set_mode((screen_width,screen_height))
        pygame.init()

    def add_to_layer(self,sprite,layer=0):
        self.__layers[layer].append(sprite)

    def __render_surface(self,sprite):
        self.__main_surface.blit(sprite.get_surface(), sprite.get_rect())

    def render_all(self):
        #Add loops to render all layers in order

        #Clear surface
        self.__main_surface.fill(self.__back_color)

        #Draw all layers on surface
        for layer in self.__layers:
            for sprite in layer:
                self.__render_surface(sprite)

        #Copy main surface to screen
        self.__screen.blit(self.__main_surface,self.__rect)


    def flip_screen(self):
        pygame.display.flip()