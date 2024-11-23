import pygame

class Sprite(pygame.sprite.Sprite):
    """
    Contains a pygame sprite
    """
    def __init__(self,x,y,width,height,image):
        super().__init__()
        self.__surface=pygame.Surface((width,height))   #Surface that renders all information
        self.__image_path=image #Path to image used
        self.__image=pygame.image.load(self.__image_path)   #Loads image from file
        self.__image=pygame.transform.scale(self.__image,(width,height))    #Stretches image
        self.__surface=self.__image #Set image to surface
        self.__rect=self.__surface.get_rect()   #Rect object for sprite dimensions
        self.__rect.x=x #Set sprite location x
        self.__rect.y=y #Set sprite location y

    #Getters:
    def rect(self):
        return self.__rect

    def image_path(self):
        return self.__image_path

    def get_x(self):
        return self.__rect.x

    def get_y(self):
        return self.__rect.y

    def get_width(self):
        return self.__rect.width

    def get_height(self):
        return self.__rect.height

    def surface(self):
        return self.__surface


    #Setters:
    def set_x(self,x):
        self.__rect.x=x

    def set_y(self,y):
        self.__rect.y=y

    def set_width(self,width):
        self.__rect.width=width

    def set_height(self,height):
        self.__rect.height=height