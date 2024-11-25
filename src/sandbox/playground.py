from src.game_objects.InfoBox import InfoBox
from src.graphics.Sprite import Sprite
from src.graphics.Renderer import Renderer
from src.globals.UC import UC


import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from src.players.Entity import Entity
from src.players.Character import Character
from src.players.Player import Player

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




renderer = Renderer(SCREEN_WIDTH,SCREEN_HEIGHT,(255,255,0))

# player1.change_character("Mina")
renderer.add_to_layer(player1)
text_box= InfoBox(0, 568, 600, 200, "Temporary text", 5,(200, 0, 0))
renderer.add_to_layer(text_box,1)
x=0
px=1024
my_text=""
while running:
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False
    px= px-2 if px>200 else px
    # player_sprite.set_x(px)
    x = x+1 if x<255 else 0
    # player_sprite.blend_color((x, 0, 0))
    my_text=(f"{my_text}{player1.current_character.get_name()} a b adfsdf dsaf sdf sdfsdfsdfsdafsf asdfa sdfOIDSFLKjf  "
             f"!")
    text_box.write_text(my_text)
    player1.change_character("Mina")

    renderer.render_all()
    renderer.flip_screen()
    clock.tick(2)