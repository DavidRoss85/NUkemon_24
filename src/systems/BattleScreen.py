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

from src.game_objects.Background import Background
from src.game_objects.BattleMenu import BattleMenu
from src.game_objects.StatBox import StatBox
from src.game_objects.InfoBox import InfoBox
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

    def __init__(self,player,enemy,renderer, animator, animation_layer):
        self.renderer=renderer
        self.player=player
        self.enemy:Computer=enemy
        self.background=Background(0,0,UC.screen_width,UC.screen_height)
        self.animation_layer=animation_layer
        self.clock=pygame.time.Clock()
        self.animator=animator


        self.fps=60

        self.running=False

        self.player_menu=None
        self.message_box=None
        self.messenger=None
        self.enemy_stat_box=None
        self.player_stat_box=None
        
        self.turn_system= TurnSystem(player,enemy,self.messenger)

        self.menu_list=[]   #this is set in set_up_interface
        self.target_menu=BattleMenu(self.DEFAULT_TARGET_MENU_X,self.DEFAULT_TARGET_MENU_Y,100,100)
        self.target_menu.set_visible(False)
        self.menu_tree=[]
        self.__queued_action = None

        #These list all the interactive objects on screen to allow user to choose to point his action
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

        #Set up the UI:
        self.set_background()
        self.set_positions()
        self.set_up_interface()
        self.update_dictionaries()



    def set_up_interface(self):
        """
        Draws and positions menus and graphical items on screen
        :return:
        """
        self.player_stat_box = StatBox(self.player, 0, 175, 400, 125)
        self.enemy_stat_box = StatBox(self.enemy, 624, 350, 400, 125)

        self.message_box = InfoBox(0, 568, 680, 200, "", 5, (1, 1, 1))
        self.player_menu = BattleMenu(681, 568, 347, 200, self.player.get_menu_dictionary())

        self.menu_list = [self.player_menu, self.target_menu]  # Maybe keep this...

        self.messenger = Messenger(self.message_box)
        self.player.set_messenger(self.messenger)
        self.enemy.set_messenger(self.messenger)
        self.turn_system.set_messenger(self.messenger)

    def set_background(self):
        """
        Set the background image
        :return:
        """
        self.background = Background(0, 0, UC.screen_width, UC.screen_height)

    def set_positions(self):
        #Update player and enemy positions
        for teammate in self.player.get_team().values():
            teammate.set_x(self.PLAYER_X)
            teammate.set_y(self.PLAYER_Y)

        self.player.set_x(self.PLAYER_X)
        self.player.set_y(self.PLAYER_Y)

        for teammate in self.enemy.get_team().values():
            teammate.set_x(self.ENEMY_X)
            teammate.set_y(self.ENEMY_Y)

        self.enemy.set_x(self.ENEMY_X)
        self.enemy.set_y(self.ENEMY_Y)

    def update_dictionaries(self):
        """
        Create and update lists for enemies and players on field
        :return:
        """
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
        """
        Create a list of all enemies on field
        :return:
        """
        td=dict()
        enemy={"owner":self.enemy, "receiver":self.enemy.get_current_character()}
        td[enemy["receiver"].get_name()]= enemy
        return td

    def list_player_team(self):
        """
        Creates a list for all inactive players on player team
        :return:
        """
        td=dict()
        for teammate in self.player.get_team().values():
            td[teammate.get_name()]={"owner":self.player, "receiver":teammate}
        del td[self.player.get_current_character().get_name()]
        return td

    def list_active_actors(self):
        """
        List of all players and enemies that can be targeted
        :return:
        """
        td=dict()
        player=self.player.get_current_character()
        enemy=self.enemy.get_current_character()
        td[player.get_name()]={"owner":self.player, "receiver":player}
        td[enemy.get_name()]={"owner":self.enemy, "receiver":enemy}
        return td

    def list_self(self):
        """
        A list for user. Used for actions that can only target the player
        :return:
        """
        td=dict()
        player={"owner":self.player, "receiver":self.player.get_current_character()}
        td[player["receiver"].get_name()] = player
        return td

    def execute_menu(self,name):
        """
        Carries out an action when user selects an item from the battle menu
        :param name: A dictionary containing either another dictionary (sub menu) or Object (target)
        :return:
        """
        items={"":""}
        self.target_menu.set_current_selection_number(0)
        if isinstance(name,dict):
            if "target" in name:
                print(name)
                items=self.target_dictionary[name["target"]]
                self.__queued_action={"name": name["name"], "function": name["function"]}
                self.target_menu.set_position(500,500)
                self.target_menu.update_menu(items, 300, len(items) * self.FONT_HEIGHT + 10)
                self.target_menu.set_visible(True)
            elif "menu" in name:
                items=name["menu"]

                self.target_menu.update_menu(items, 300,len(items)*self.FONT_HEIGHT +10 )
                self.target_menu.set_visible(True)

            else:
                print("EXECUTE")
                print(f"Battle Screen: {name["receiver"].get_name()}")
                self.menu_tree.clear()
                self.target_menu.set_visible(False) #Hide menu

                self.perform_action(self.player,self.__queued_action,name)

                self.turn_system.set_player_turn(False) #Switch to enemy turn

    def perform_action(self, subject, verb, o_ject):
        o_ject["owner"].freeze_frame()

        # Execute the stored function on the target (current_character)
        verb["function"](o_ject["receiver"])
        print(verb)

        # Add and animation the paused animation queue
        # Game events will wait for these animations to complete
        self.animator.pause_and_animate({
            "subject": subject,
            "action": verb["name"]
        })

        self.animator.pause_and_animate({
            "object": o_ject["owner"],
            "action": verb["name"]
        })


    def create_layers(self,renderer:Renderer):
        """
        Adds all the layers to the renderer in a specific order
        :param renderer: The Renderer object that draws on the screen
        :return:
        """
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

    def listen_for_input(self,event_list):
        """
        Listens for key presses from the user
        :param event_list: List of key/window events passed by pygame
        :return:
        """
        player_turn = self.turn_system.get_player_turn()
        for event in event_list:
            if player_turn and event.type == KEYDOWN and not self.animator.animating:
                match event.key:
                    case btn.K_ESCAPE:
                        self.running=False
                    case btn.K_LEFT:
                        pass
                        # self.player.change_character()
                    case btn.K_RIGHT:
                        pass
                        self.player.change_character(self.player.get_team()["Mina"])
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
                self.running = False

    def perform_updates(self):
        """
        Update every cycle
        :return:
        """
        self.update_dictionaries()
        self.messenger.stream_text()
        self.animator.animate_list()
        self.turn_system.check_loss_conditions(self.perform_action)
        if self.turn_system.check_win_conditions(self.perform_action):
            pass

    def start(self):
        """
        Main Battle loop
        :return:
        """
        self.running=True
        # self.turn_system.set_player_turn(False)
        while self.running:
            player_turn=self.turn_system.get_player_turn()
            animating=self.animator.get_animating_status()

            self.perform_updates()
            game_events=pygame.event.get()
            self.listen_for_input(game_events)
            if not player_turn and not animating:
                self.turn_system.cpu_perform_action(self.perform_action)

            self.renderer.render_all()
            self.renderer.flip_screen()
            self.clock.tick(self.fps)

