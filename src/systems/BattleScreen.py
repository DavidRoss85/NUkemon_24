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

from src.game_objects.BattleMenu import BattleMenu
from src.graphics.Renderer import Renderer
from src.globals.UC import *

class BattleScreen:
    DEFAULT_TARGET_MENU_X=300
    DEFAULT_TARGET_MENU_Y=400
    FONT_HEIGHT=UC.default_font_pixel_height

    def __init__(self,player,enemy,message_box,player_menu,player_stat_box,enemy_stat_box,background,animation_layer):
        self.player=player
        self.enemy=enemy
        self.message_box=message_box
        self.player_menu=player_menu
        self.enemy_stat_box=enemy_stat_box
        self.player_stat_box=player_stat_box
        self.background=background
        self.animation_layer=animation_layer

        self.target_menu=BattleMenu(self.DEFAULT_TARGET_MENU_X,self.DEFAULT_TARGET_MENU_Y,100,100)
        self.target_menu.set_visible(False)
        self.menu_list=[self.player_menu,self.target_menu] #Maybe keep this...
        self.menu_tree=[]
        self.__queued_action = None

        self.enemy_dict=dict()
        self.team_dict=dict()
        self.active_dict=dict()
        self.self_dict=dict()

        self.target_dictionary={
            "enemies": self.enemy_dict,
            "team": self.team_dict,
            "active": self.active_dict,
            "self": self.self_dict
        }
        self.update_dictionaries()

    def update_dictionaries(self):
        self.enemy_dict=self.list_enemies()
        self.team_dict=self.list_player_team()
        self.active_dict= self.list_active_actors()
        self.self_dict=self.list_self()
        self.target_dictionary={
            "enemies": self.enemy_dict,
            "team": self.team_dict,
            "active": self.active_dict,
            "self": self.self_dict
        }


    def list_enemies(self):
        td=dict()
        enemy=self.enemy.get_current_character()
        td[enemy.get_name()]= enemy
        return td

    def list_player_team(self):
        td=dict()
        td=self.player.get_team().copy()
        del td[self.player.get_current_character().get_name()]
        return td

    def list_active_actors(self):
        td=dict()
        player=self.player.get_current_character()
        enemy=self.enemy.get_current_character()
        td[player.get_name()]=player
        td[enemy.get_name()]=enemy
        return td

    def list_self(self):
        td=dict()
        player=self.player.get_current_character()
        td[player.get_name()] = player
        return td

    def execute_menu(self,name):

        items={"":""}
        self.target_menu.set_current_selection_number(0)
        if isinstance(name,dict):
            if "target" in name:
                print(name)
                items=self.target_dictionary[name["target"]]
                self.__queued_action=name["function"]
                self.target_menu.set_position(500,500)
            elif "menu" in name:
                items=name["menu"]

            self.target_menu.update_menu(items, 300,len(items)*self.FONT_HEIGHT +10 )
            self.target_menu.set_visible(True)

        else:
            print("EXECUTE")
            self.__queued_action(name)
            print(name)
            self.menu_tree.clear()
            self.target_menu.set_visible(False)


    def create_layers(self,renderer:Renderer):
        #Add all objects to layers
        renderer.add_to_layer(self.background)
        renderer.add_to_layer(self.enemy,1)
        renderer.add_to_layer(self.player,1)
        renderer.add_to_layer(self.enemy_stat_box,2)
        renderer.add_to_layer(self.player_stat_box,2)
        renderer.add_to_layer(self.message_box,2)
        renderer.add_to_layer(self.player_menu,3)
        renderer.add_to_layer(self.target_menu,3)
        # renderer.add_to_layer(effectslayer,4)

    def listen_for_input(self,event):
        if event.type == KEYDOWN:
            match event.key:
                case btn.K_ESCAPE:
                    running=False
                case btn.K_LEFT:
                    pass
                    # self.player.change_character()
                case btn.K_RIGHT:
                    pass
                    # self.player.change_character()
                case btn.K_UP:
                    self.menu_list[self.target_menu.get_visible()].prev_menu_item()
                case btn.K_DOWN:
                    self.menu_list[self.target_menu.get_visible()].next_menu_item()
                case btn.K_BACKSPACE:

                    self.__queued_action=None
                    if len(self.menu_tree)>0:
                        self.menu_tree.pop()

                    if len(self.menu_tree)==0:
                        self.target_menu.set_visible(False)
                    else:
                        self.execute_menu(self.menu_tree[-1])


                case btn.K_RETURN:
                    name=0
                    self.player.get_menu_dictionary()
                    if len(self.menu_tree)==0:
                        name=self.menu_list[0].get_current_selection()
                    else:
                        name = self.menu_list[1].get_current_selection()
                    # print(f"Battle Screen: {self.menu_tree}")
                    self.menu_tree.append(name)
                    self.execute_menu(name)



        elif event.type == QUIT:
            running = False

    def perform_updates(self):
        self.update_dictionaries()
