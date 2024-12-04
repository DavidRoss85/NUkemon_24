import pygame
import pygame.locals as btn
from pygame.locals import (
    KEYDOWN,
    QUIT,
)

from src.game_objects.Background import Background
from src.game_objects.BattleMenu import BattleMenu
from src.game_objects.Overlay import Overlay
from src.game_objects.StatBox import StatBox
from src.game_objects.InfoBox import InfoBox
from src.graphics.Sprite import Sprite
from src.players.Computer import Computer
from src.systems.Messenger import Messenger


from src.graphics.Renderer import Renderer
from src.globals.UC import *
from src.systems.TurnSystem import TurnSystem


class BattleScreen:
    DEFAULT_TARGET_MENU_X=300
    DEFAULT_TARGET_MENU_Y=400
    PLAYER_X=100
    PLAYER_Y=300
    ENEMY_X=600
    ENEMY_Y=50
    FONT_HEIGHT=UC.default_font_pixel_height

    def __init__(self,player,enemy,renderer, animator):
        self.__renderer=renderer
        self.__player=player
        self.__enemy:Computer=enemy
        self.__background=Background(0, 0, UC.screen_width, UC.screen_height)
        self.__animation_layer=Overlay(0,0,UC.screen_width,UC.screen_height)
        self.__clock=pygame.time.Clock()
        self.__animator=animator


        self.__fps=120
        self.__intro_started=False

        self.__running=False

        self.__player_menu=None
        self.__message_box=None
        self.__messenger=None
        self.__enemy_stat_box=None
        self.__player_stat_box=None
        
        self.__turn_system= TurnSystem(player, enemy, self.__messenger)

        self.__menu_list=[]   #this is set in set_up_interface
        self.__target_menu=BattleMenu(self.DEFAULT_TARGET_MENU_X, self.DEFAULT_TARGET_MENU_Y, 100, 100)
        self.__target_menu.set_visible(False)
        self.__menu_tree=[]
        self.__queued_action = None

        #These list all the interactive objects on screen to allow user to choose to point his action
        self.__enemy_dict=dict()
        self.__team_dict=dict()
        self.__active_dict=dict()
        self.__self_dict=dict()

        self.__target_dictionary={
            "enemies": self.__enemy_dict,
            "team": self.__team_dict,
            "active": self.__active_dict,
            "self": self.__self_dict
        }

        #Set up the UI:
        self.set_background()
        self.__set_up_interface()
        self.__set_positions()
        self.update_dictionaries()


    #=======================================================================================================
    def __set_up_interface(self):
        """
        Draws and positions menus and graphical items on screen
        :return:
        """
        self.__player_stat_box = StatBox(self.__player, 0, 175, 400, 125)
        self.__enemy_stat_box = StatBox(self.__enemy, 624, 350, 400, 125)

        self.__message_box = InfoBox(0, 568, 680, 200, "", 5, (1, 1, 1))
        self.__player_menu = BattleMenu(681, 568, 347, 200, self.__player.get_menu_dictionary())

        self.__menu_list = [self.__player_menu, self.__target_menu]  # Maybe keep this...

        self.__messenger = Messenger(self.__message_box)
        self.__player.set_messenger(self.__messenger)
        self.__enemy.set_messenger(self.__messenger)
        self.__turn_system.set_messenger(self.__messenger)

        self.__enemy.set_animator(self.__animator)

        self.__animator.update_object_dictionary({
            "enemy_stat_box":self.__enemy_stat_box,
            "player_stat_box": self.__player_stat_box,
            "player_menu_box": self.__player_menu,
            "message_box": self.__message_box,
            "messenger":self.__messenger,
            "player":self.__player,
            "enemy": self.__enemy,
            "background":self.__background,
            "animation_layer":self.__animation_layer
        })

    # =======================================================================================================
    def set_background(self, image=None):
        """
        Set the __background image
        :return:
        """
        back_width=2067 #UC.screen_width*1.1
        back_height=1162 #UC.screen_height
        x_offset=(back_width-UC.screen_width)/4
        y_offset=(back_height-UC.screen_height)/2
        self.__background = Background(-x_offset, -y_offset, back_width, back_height,image)

    # =======================================================================================================
    def __set_positions(self):
        #Update __player and __enemy positions
        for teammate in self.__player.get_team().values():
            teammate.set_x(self.PLAYER_X)
            teammate.set_y(self.PLAYER_Y)

        self.__player.set_x(self.PLAYER_X)
        self.__player.set_y(self.PLAYER_Y)

        for teammate in self.__enemy.get_team().values():
            teammate.set_x(self.ENEMY_X)
            teammate.set_y(self.ENEMY_Y)

        self.__enemy.set_x(self.ENEMY_X)
        self.__enemy.set_y(self.ENEMY_Y)

    # =======================================================================================================
    def update_dictionaries(self):
        """
        Create and update lists for enemies and players on field
        :return:
        """
        self.__enemy_dict= self.__list_enemies()
        self.__team_dict= self.__list_player_team()
        self.__active_dict= self.__list_active_actors()
        self.__self_dict= self.__list_self()
        self.__target_dictionary={
            "enemies": self.__enemy_dict,
            "team": self.__team_dict,
            "active": self.__active_dict,
            "self": self.__self_dict
        }

    # =======================================================================================================
    def __list_enemies(self):
        """
        Create a list of all enemies on field
        :return:
        """
        td=dict()
        enemy={"owner":self.__enemy, "receiver":self.__enemy.get_current_character()}
        td[enemy["receiver"].get_name()]= enemy
        return td

    # =======================================================================================================
    def __list_player_team(self):
        """
        Creates a list for all inactive players on __player team
        :return:
        """
        td=dict()
        for teammate in self.__player.get_team().values():
            td[teammate.get_name()]={"owner":self.__player, "receiver":teammate}
        del td[self.__player.get_current_character().get_name()]
        return td
    # =======================================================================================================
    def __list_player_graveyard(self):
        """
        Creates a list for all inactive players on __player team
        :return:
        """
        td = dict()
        for teammate in self.__player.get_graveyard().values():
            td[teammate.get_name()] = {"owner": self.__player, "receiver": teammate}
        return td
    # =======================================================================================================
    def __list_active_actors(self):
        """
        List of all players and enemies that can be targeted
        :return:
        """
        td=dict()
        player=self.__player.get_current_character()
        enemy=self.__enemy.get_current_character()
        td[enemy.get_name()]={"owner":self.__enemy, "receiver":enemy}
        td[player.get_name()]={"owner":self.__player, "receiver":player}
        return td

    # =======================================================================================================
    def __list_self(self):
        """
        A list for user. Used for actions that can only target the __player
        :return:
        """
        td=dict()
        player={"owner":self.__player, "receiver":self.__player.get_current_character()}
        td[player["receiver"].get_name()] = player
        return td
    # =======================================================================================================
    def create_layers(self,renderer:Renderer):
        """
        Adds all the layers to the __renderer in a specific order
        :param renderer: The Renderer object that draws on the screen
        :return:
        """
        #Add all objects to layers
        renderer.add_to_layer(self.__background)
        renderer.add_to_layer(self.__enemy, 1)
        renderer.add_to_layer(self.__player, 1)
        renderer.add_to_layer(self.__enemy_stat_box, 2)
        renderer.add_to_layer(self.__player_stat_box, 2)
        renderer.add_to_layer(self.__message_box, 2)
        renderer.add_to_layer(self.__player_menu, 3)
        renderer.add_to_layer(self.__target_menu, 3)
        renderer.add_to_layer(self.__animation_layer,4)

    # =======================================================================================================
    def execute_menu(self,name):
        """
        Carries out an action when user selects an item from the battle menu
        :param name: A dictionary containing either another dictionary (sub menu) or Object (target)
        :return:
        """
        items={"":""}
        self.__target_menu.set_current_selection_number(0)
        if isinstance(name,dict):
            if "target" in name:

                items=self.__target_dictionary[name["target"]]
                self.__queued_action={"name": name["name"], "function": name["function"]}
                self.__target_menu.set_position(500, 500)
                self.__target_menu.update_menu(items, 300, len(items) * self.FONT_HEIGHT + 10)
                self.__target_menu.set_visible(True)
            elif "menu" in name:
                items=name["menu"]

                self.__target_menu.update_menu(items, 300, len(items) * self.FONT_HEIGHT + 10)
                self.__target_menu.set_visible(True)

            else:
                #Clear the menu tree, returning to main menu:
                self.__menu_tree.clear()
                self.__target_menu.set_visible(False) #Hide menu
                #Execute action from in the dictionary:
                self.perform_action(self.__player, self.__queued_action, name)
                for team_member in self.__player.get_team().values():
                    TurnSystem.evaluate_status(team_member,team_member==self.__player.get_current_character())
                self.__turn_system.set_player_turn(False) #Switch to __enemy turn



    # =======================================================================================================
    def perform_action(self, subject, verb, o_ject):
        o_ject["owner"].freeze_frame()

        # Execute the stored function on the target (current_character)
        owner=verb["function"](o_ject["receiver"])

        # Add and animation the paused animation __queue
        # Game events will wait for these animations to complete
        self.__animator.pause_and_animate({
            "subject": subject,
            "action": verb["name"]
        })

        self.__animator.pause_and_animate({
            "object": owner,
            "action": verb["name"]
        })


    # =======================================================================================================
    def listen_for_input(self,event_list):
        """
        Listens for key presses from the user
        :param event_list: List of key/window events passed by pygame
        :return:
        """
        player_turn = self.__turn_system.get_player_turn()
        for event in event_list:
            if player_turn and event.type == KEYDOWN and not self.__animator.get_animating_status():
                match event.key:
                    case btn.K_ESCAPE:
                        self.__running=False
                    case btn.K_LEFT:
                        pass
                        # self.__player.change_character()
                    case btn.K_RIGHT:
                        pass
                        # self.__player.change_character(self.__player.get_team()["Mina"])
                    case btn.K_UP:
                        self.__menu_list[self.__target_menu.get_visible()].prev_menu_item()
                    case btn.K_DOWN:
                        self.__menu_list[self.__target_menu.get_visible()].next_menu_item()
                    case btn.K_BACKSPACE:

                        self.__queued_action=None
                        if len(self.__menu_tree)>0:
                            self.__menu_tree.pop()

                        if len(self.__menu_tree)==0:
                            self.__target_menu.set_visible(False)
                        else:
                            self.execute_menu(self.__menu_tree[-1])

                    case btn.K_RETURN:
                        name=0
                        self.__player.get_menu_dictionary()
                        if len(self.__menu_tree)==0:
                            name=self.__menu_list[0].get_current_selection()
                        else:
                            name = self.__menu_list[1].get_current_selection()
                        # print(f"Battle Screen: {self.__menu_tree}")
                        self.__menu_tree.append(name)
                        self.execute_menu(name)



            elif event.type == QUIT:
                self.__running = False

    # =======================================================================================================
    def perform_updates(self):
        """
        Update every cycle
        :return:
        """
        self.update_dictionaries()
        self.__player_menu.update_menu(self.__player.get_menu_dictionary())
        self.__messenger.stream_text()
        self.__animator.animate_list()
        self.__turn_system.check_loss_conditions(self.perform_action)
        if self.__turn_system.check_win_conditions(self.perform_action):
            pass

    # =======================================================================================================
    def show_battle_intro(self):
        self.__animator.pause_and_animate({"action":"Intro","subject":"errbody"})

    # =======================================================================================================
    def start(self):
        """
        Main Battle loop
        :return:
        """
        self.__running=True
        # self.show_battle_intro()

        # self.__turn_system.set_player_turn(False)
        while self.__running:
            player_turn=self.__turn_system.get_player_turn()
            animating=self.__animator.get_animating_status()


            self.perform_updates()
            game_events=pygame.event.get()
            self.listen_for_input(game_events)
            if not player_turn and not animating:
                self.__turn_system.cpu_perform_action(self.perform_action)

            self.__renderer.render_all()
            self.__renderer.flip_screen()
            self.__clock.tick(self.__fps)

