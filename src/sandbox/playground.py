"""
This module is for testing:
"""

import pygame
import sys
import os

from src.graphics.Sprite import Sprite

sys.path.insert(0,os.path.join(os.path.dirname(__file__),'../..'))


from src.globals.UC import UC
from src.globals.personas import Personas, Crews
from src.systems.BattleScreen import BattleScreen
from src.systems.BattleAnimator import BattleAnimator
from src.graphics.Renderer import Renderer
from src.sound.sound import Sound

from src.players.Player import Player
from src.players.Computer import Computer

# #Uncomment this code to count lines in project:
# from src.utils.utils import count_lines_in_project
# x=count_lines_in_project(UC.absolute_path)
# print(f"Total lines of code in project: {x}")
# exit(0)


SCREEN_WIDTH = UC.screen_width
SCREEN_HEIGHT = UC.screen_height

renderer = Renderer(SCREEN_WIDTH,SCREEN_HEIGHT,UC.game_back_color)
# sound_dict={"boop":"boop.wav","punch":"/effects/punch-classic-betacut.mp3"}
# battle_music=f"rivalry-sulyya.mp3"
music_mixer= Sound(music_volume=0.6, music_file=UC.battle_music)
sound_mixer= Sound(effect_volume=1,sound_dict=UC.animator_sound_dictionary)
# animator=BattleAnimator(mixer)

player1=Player()
enemy1=Computer()

player1.set_team(Crews.default_player)
enemy1.set_team(Crews.default_enemy)


battle_screen= BattleScreen(player1, enemy1, renderer, music_mixer,sound_mixer )
battle_screen.create_layers(renderer)
battle_screen.set_previous_screen(Sprite(0,0,UC.screen_width,UC.screen_height,UC.background_image))

battle_screen.start()
