from src.game_objects.BattleMenu import BattleMenu
from src.systems.BattleScreen import BattleScreen
from src.game_objects.InfoBox import InfoBox
from src.graphics.Sprite import Sprite
from src.graphics.Renderer import Renderer
from src.globals.UC import UC


import pygame
from pygame.locals import (
    QUIT,
)

from src.Units.Character import Character
from src.players.Human import Player
from src.systems.Messenger import Messenger

SCREEN_WIDTH = UC.screen_width
SCREEN_HEIGHT = UC.screen_height

running=True
clock=pygame.time.Clock()

player_sprite1=Sprite(200, 400, 200, 200, "../assets/images/test_images/Boy_backpack1_hmmm_bk.png", (64, 177, 64), (0, 0, 200))
player_sprite2=Sprite(200, 400, 200, 200, "../assets/images/test_images/Emoji-Chill.png", (64, 177, 64), (0, 0, 200))

enemy_sprite1=Sprite(200, 400, 100, 100, "../assets/images/test_images/Emoji-On-Fire.png", (64, 177, 64), (0, 0, 200))

playable_character1=Character("Rory", 1, 150, 150, 10, 10,player_sprite1)
playable_character2=Character("Mina", 1, 100, 200, 5, 15,player_sprite2)
playable_character3=Character("Chris", 1, 200, 100, 15, 5,player_sprite1)

enemy_character1=Character("Wendie",1,200,200,5,5,enemy_sprite1,600,200)

player1=Player()
player1.set_x(200)
player1.set_y(400)
player1.add_team_member(playable_character1)
player1.add_team_member(playable_character2)
player1.add_team_member(playable_character3)

enemy1=Player()
enemy1.set_x(600)
enemy1.set_y(200)
enemy1.add_team_member(enemy_character1)

renderer = Renderer(SCREEN_WIDTH,SCREEN_HEIGHT,(255,255,0))

text_box= InfoBox(0, 568, 680, 200, "Temporary text", 5,(200, 0, 0))
user_menu=BattleMenu(681, 568, 347, 200, player1.get_menu_list())
messenger=Messenger(text_box)
player1.set_messenger(messenger)
enemy1.set_messenger(messenger)

battle_screen=BattleScreen(player1,enemy1,text_box,user_menu,0,0,0,0)
battle_screen.create_layers(renderer)

player1.get_current_character().set_max_hp(1500)

x=0
px=1024
my_text=""
while running:
    for event in pygame.event.get():
        battle_screen.listen_for_input(event)
        # Did the user click the window close button? If so, stop the loop.
        if event.type == QUIT:
            running = False


    px= px-2 if px>200 else px

    x = x+1 if x<255 else 0

    player1.set_curr_hp(px)
    messenger.stream_text()
    # my_text=f"Your health: {player1.get_curr_hp()}\n \n \n \n"
    # text_box.write_text(my_text)

    renderer.render_all()
    renderer.flip_screen()
    clock.tick(30)