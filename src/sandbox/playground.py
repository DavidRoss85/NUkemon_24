from src.game_objects.Background import Background
from src.game_objects.BattleMenu import BattleMenu
from src.game_objects.StatBox import StatBox
from src.globals.personas import Personas, Crews
from src.systems.BattleScreen import BattleScreen
from src.game_objects.InfoBox import InfoBox
from src.graphics.Sprite import Sprite
from src.graphics.Renderer import Renderer
from src.globals.UC import UC


import pygame
from pygame.locals import (
    QUIT,
)


from src.players.Human import Player

SCREEN_WIDTH = UC.screen_width
SCREEN_HEIGHT = UC.screen_height

running=True
clock=pygame.time.Clock()

renderer = Renderer(SCREEN_WIDTH,SCREEN_HEIGHT,(255,255,0))


player1=Player()
enemy1=Player()

player1.set_team(Crews.default_player)
enemy1.set_team(Crews.default_enemy)


battle_screen= BattleScreen(player1, enemy1, 0)
battle_screen.create_layers(renderer)

player1.get_current_character().set_max_hp(1500)
player1.get_current_character().set_curr_hp(1500)


while running:

    battle_screen.perform_updates()
    for event in pygame.event.get():
        battle_screen.listen_for_input(event)
        # Did the user click the window close button? If so, stop the loop.
        if event.type == QUIT:
            running = False


    renderer.render_all()
    renderer.flip_screen()
    clock.tick(30)