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

from src.graphics.Renderer import Renderer


class BattleScreen:
    def __init__(self,player,enemy,message_box,player_menu,player_stat_box,enemy_stat_box,background,animation_layer):
        self.player=player
        self.enemy=enemy
        self.message_box=message_box
        self.player_menu=player_menu
        self.enemy_stat_box=enemy_stat_box
        self.player_stat_box=player_stat_box
        self.background=background
        self.animation_layer=animation_layer

    def create_layers(self,renderer:Renderer):
        #Add all objects to layers
        # renderer.add_to_layer(background)
        renderer.add_to_layer(self.enemy,1)
        renderer.add_to_layer(self.player,1)
        # renderer.add_to_layer(enemylifbar,2)
        # renderer.add_to_layer(playerlifbar,2)
        renderer.add_to_layer(self.message_box,2)
        renderer.add_to_layer(self.player_menu,3)
        # renderer.add_to_layer(effectslayer,4)

    def listen_for_input(self,event):
        if event.type == KEYDOWN:
            match event.key:
                case btn.K_ESCAPE:
                    running=False
                case btn.K_LEFT:
                    pass
                    self.player.change_character()
                case btn.K_RIGHT:
                    pass
                    self.player.change_character()
                case btn.K_UP:
                    self.player_menu.prev_menu_item()
                case btn.K_DOWN:
                    self.player_menu.next_menu_item()
                case btn.K_RETURN:
                    self.player.test_set_target(self.enemy.get_current_character())
                    self.player.execute_menu_item(self.player_menu.get_current_selection())
                    self.player_menu.update_menu(self.player.get_menu_list())
        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False