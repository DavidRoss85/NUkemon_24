import pygame
import sys
import os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'../..'))


from src.globals.UC import UC
from src.globals.personas import Personas, Crews
from src.systems.BattleScreen import BattleScreen
from src.systems.Animator import Animator
from src.graphics.Renderer import Renderer

from src.players.Human import Player
from src.players.Computer import Computer

# #Uncomment this code to count lines in project:
# from src.utils.utils import count_lines_in_project
# x=count_lines_in_project(UC.absolute_path)
# print(f"Total lines of code in project: {x}")
# exit(0)


SCREEN_WIDTH = UC.screen_width
SCREEN_HEIGHT = UC.screen_height

renderer = Renderer(SCREEN_WIDTH,SCREEN_HEIGHT,UC.game_back_color)
animator=Animator()

player1=Player()
enemy1=Computer()

player1.set_team(Crews.default_player)
enemy1.set_team(Crews.default_enemy)


battle_screen= BattleScreen(player1, enemy1, renderer, animator)
battle_screen.create_layers(renderer)


battle_screen.start()
