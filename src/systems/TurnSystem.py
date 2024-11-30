import pygame

from src.game_objects.Background import Background
from src.game_objects.BattleMenu import BattleMenu
from src.game_objects.StatBox import StatBox
from src.systems.BattleScreen import BattleScreen
from src.game_objects.InfoBox import InfoBox
from src.graphics.Sprite import Sprite
from src.graphics.Renderer import Renderer
from src.globals.UC import UC

from pygame.locals import (
    QUIT,
)

from src.Units.Character import Character
from src.players.Human import Player
from src.systems.Messenger import Messenger



class TurnSystem:
    def __init__(self):
        self.__player_turn=False
        self.__battle_running=False
        self.__player=None
        self.__enemy=None
        self.__enemy_x=800
        self.__enemy_y=200
        self.__player_x=100
        self.__player_y=300



    def start_battle(self,value=False):
        self.__battle_running=value

        while self.__battle_running:
            pass
