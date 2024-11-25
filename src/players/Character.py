from src.graphics.Sprite import Sprite
from src.players.Entity import Entity

class Character(Entity):
    def __init__(self,name,level,hp,mp,strength,intel,sprite,x=0,y=0):
        super().__init__(name,level,hp,mp,strength,intel)
        self.sprite:Sprite=sprite
        self.x_coord=x
        self.y_coord=y


    #Getters
    def get_x(self):
        return self.x_coord

    def get_y(self):
        return self.y_coord

    def get_sprite(self):
        return self.sprite

    #Setters
    def set_x(self,x):
        self.x_coord=x

    def set_y(self,y):
        self.y_coord=y