from src.game_objects.BattleMenu import BattleMenu
from src.game_objects.BattleScreen import BattleScreen
from src.game_objects.InfoBox import InfoBox
from src.graphics.Sprite import Sprite
from src.graphics.Renderer import Renderer
from src.globals.UC import UC


import pygame
import pygame.locals as btn
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from src.Units.Character import Character
from src.players.Human import Player

SCREEN_WIDTH = UC.screen_width
SCREEN_HEIGHT = UC.screen_height

running=True
clock=pygame.time.Clock()

player_sprite1=Sprite(200, 400, 200, 200, "../assets/images/test_images/Boy_backpack1_hmmm_bk.png", (64, 177, 64), (0, 0, 200))
enemy_sprite1=Sprite(200, 400, 100, 100, "../assets/images/test_images/Emoji-On-Fire.png", (64, 177, 64), (0, 0, 200))

playable_character1=Character("Rory", 1, 150, 150, 10, 10,player_sprite1)
playable_character2=Character("Mina", 1, 100, 200, 5, 15,enemy_sprite1)
playable_character3=Character("Chris", 1, 200, 100, 15, 5,player_sprite1)


player1=Player()
player1.add_team_member(playable_character1)
player1.add_team_member(playable_character2)
player1.add_team_member(playable_character3)
print(player1.update_move_list())

renderer = Renderer(SCREEN_WIDTH,SCREEN_HEIGHT,(255,255,0))

text_box= InfoBox(0, 568, 680, 200, "Temporary text", 5,(200, 0, 0))
user_menu=BattleMenu(681,568,347,200,player1.update_move_list())


battle_screen=BattleScreen(player1,0,text_box,user_menu,0,0,0,0)
battle_screen.create_layers(renderer)

player1.get_current_character().set_max_hp(1500)
# renderer.add_to_layer(player1)
# renderer.add_to_layer(text_box,1)
x=0
px=1024
my_text=""
while running:
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            match event.key:
                case btn.K_ESCAPE:
                    running=False
                case btn.K_LEFT:
                    player1.change_character("Mina")
                case btn.K_RIGHT:
                    player1.change_character("Rory")
                case btn.K_UP:
                    user_menu.set_current_selection(0)
                case btn.K_DOWN:
                    user_menu.set_current_selection(1)


        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False
    px= px-2 if px>200 else px
    # player_sprite.set_x(px)
    x = x+1 if x<255 else 0
    # player_sprite.blend_color((x, 0, 0))
    player1.set_curr_hp(px)
    my_text=f"Your health: {player1.get_curr_hp()}\n \n \n \n"
    text_box.write_text(my_text)

    renderer.render_all()
    renderer.flip_screen()
    clock.tick(10)