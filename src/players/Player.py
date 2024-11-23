from src.globals.UC import UC

from src.graphics.Sprite import Sprite
from src.players.Character import Character


class Player:
    def __init__(self,character:Character, sprite:Sprite):
        self.__sprite=sprite
        self.__character=character
