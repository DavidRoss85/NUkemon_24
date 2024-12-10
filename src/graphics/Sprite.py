from src.globals.UC import UC

MASK = UC.image_mask_color

import pygame
from pygame.locals import RLEACCEL


class Sprite(pygame.sprite.Sprite):
    """
    Inherits from Pygame's Sprite object
    Sprite Objects handle all information regarding the image to be rendered
    including masking (transparency), blending colors, resizing, and stretching
    of images on the screen. Final product is a pygame surface which can be drawn
    onto the screen.
    """

    def __init__(self, x, y, width, height, image=None, mask_color=MASK, blend_color: tuple = None,
                 stretch: bool = True):
        super().__init__()
        self.__surface = pygame.Surface((width, height))  #Surface that renders all information
        if image is not None:
            self.__image_path = image  #Path to image used
            self.__image = pygame.image.load(self.__image_path)  #Loads image from file
            if stretch:
                self.__image = pygame.transform.scale(self.__image, (width, height))  #Stretches image
            else:
                self.__surface = pygame.Surface((self.__image.get_width(), self.__image.get_height()))
            self.__surface = self.__image  #Set image to surface
        else:
            self.__surface.fill((0, 0, 0))  #All black surface

        self.__surface.set_colorkey(mask_color, RLEACCEL)  #Set transparent __color
        self.__mask_color = mask_color

        #If user specified blend:
        if blend_color is not None:
            self.__surface.fill(blend_color, special_flags=pygame.BLEND_ADD)  # For blending colors
            #Recalculate MASK __color:
            new_mask = self.__blend_mask(blend_color, self.__mask_color)
            #Re apply MASK for transparent sections
            self.__surface.set_colorkey(new_mask, RLEACCEL)
            self.__mask_color = new_mask

        self.__original_surface = self.__surface.copy()  #Keep a copy of the original created surface
        self.__rect = self.__surface.get_rect()  #Rect object for __sprite dimensions
        self.__rect.x = x  #Set __sprite location x
        self.__rect.y = y  #Set __sprite location y

    #Getters:
    def get_rect(self):
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

    def get_surface(self):
        return self.__surface

    def get_mask(self):
        return self.__mask_color

    #Setters:
    def set_x(self, x):
        self.__rect.x = x

    def set_y(self, y):
        self.__rect.y = y

    def set_width(self, width):
        self.__rect.width = width

    def set_height(self, height):
        self.__rect.height = height

    def set_alpha(self,alpha):
        if alpha<0: alpha=0
        if alpha>255: alpha=255
        self.__surface.set_alpha(alpha)

    def set_new_default(self):
        """
        Copies the current state of the __sprite into the original surface
        Calling restore after this will return the __sprite to this form
        :return:
        """
        self.__original_surface = self.__surface.copy()  # Make whatever the image is the new default

    def draw_on_surface(self, surface: pygame.Surface, x=0, y=0,scale:bool=False):
        """
        Draw another surface onto the __sprite
        :param scale: Boolean decides if to scale the surface
        :param surface: pre-rendered surface to overlay
        :param x: relative x location
        :param y: relative y location
        :return:
        """
        new_surf=surface.copy()

        #Stretches/shrinks the new image onto the surface if this is toggled on:
        if scale:
            new_surf=pygame.transform.scale(new_surf,(self.__rect.width,self.__rect.height))

        rect = new_surf.get_rect()
        rect.x = x
        rect.y = y
        #Draw sprite onto this surface
        self.__surface.blit(new_surf, rect)

    def restore(self):
        """
        Returns the __sprite to its original construction
        :return:
        """
        self.__surface = self.__original_surface.copy()

    def blend_color(self, blend_color: tuple = (0, 0, 0)):
        """
        Changes the tint/__color of the object
        :param blend_color: tuple(R,G,B)
        :return:
        """
        self.__surface = self.__original_surface.copy()
        self.__surface.fill(blend_color, special_flags=pygame.BLEND_ADD)  # For blending colors
        new_mask = self.__blend_mask(blend_color, self.__mask_color)

        self.__surface.set_colorkey(new_mask, RLEACCEL)

    def __blend_mask(self, blend_color: tuple, mask_color: tuple) -> tuple:
        """
        Returns new MASK __color for maintaining transparency features
        :param blend_color: tuple(R,G,B)
        :param mask_color: tuple(R,G,B)
        :return: tuple - new MASK (R,G,B)
        """
        new_mask = (min(blend_color[0] + mask_color[0], 255),
                    min(blend_color[1] + mask_color[1], 255),
                    min(blend_color[2] + mask_color[2], 255))

        return new_mask
