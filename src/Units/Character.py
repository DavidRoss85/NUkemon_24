from src.graphics.Sprite import Sprite
from src.Units.Entity import Entity

class Character(Entity):
    def __init__(self,name,level,hp,mp,strength,intel,sprite,x=0,y=0):
        super().__init__(name,level,hp,mp,strength,intel)
        self.sprite:Sprite=sprite
        self.__x=x
        self.__y=y


    #Getters
    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_sprite(self):
        return self.sprite

    #Setters
    def set_x(self,x):
        self.__x=x

    def set_y(self,y):
        self.__y=y