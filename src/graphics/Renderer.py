import pygame


class Renderer:
    def __init__(self,screen_width=100,screen_height=100):
        self.__top_layer_items=[]
        self.__mid_layer_items=[]
        self.__bot_layer_items=[]
        self.__main_surface=pygame.Surface((screen_width,screen_height))
        self.__main_surface.fill((0,0,0))

    def __render_surface(self,sprite=None):
        #General idea here:
        print("Render surface")
        # self.__main_surface.blit(item.surface,item.rect)
        #



    def render_all(self):
        #Add loops to render all layers in order
        print("Render all")
        for item in self.__bot_layer_items:
            self.__render_surface(item)
        for item in self.__mid_layer_items:
            self.__render_surface(item)
        for item in self.__top_layer_items:
            self.__render_surface(item)
