import pygame
import pygame.locals as btn
from pygame.locals import (
    KEYDOWN,
    QUIT,
)

from src.game_objects.Background import Background
from src.game_objects.BattleMenu import BattleMenu
from src.game_objects.HelpBox import HelpBox
from src.game_objects.Overlay import Overlay
from src.game_objects.StatBox import StatBox
from src.game_objects.InfoBox import InfoBox
from src.game_objects.Effect import Effect
from src.graphics.Sprite import Sprite
from src.players.Computer import Computer
from src.systems.BattleAnimator import BattleAnimator
from src.systems.Messenger import Messenger


from src.graphics.Renderer import Renderer
from src.globals.UC import *
from src.systems.TurnSystem import TurnSystem


class BattleScreen:
    """
    This is the object where the main battle occurs.
    This contains the player, enemy, all the battle objects, the turn system etc
    Main battle loop is at the bottom
    """
    DEFAULT_TARGET_MENU_X=300
    DEFAULT_TARGET_MENU_Y=400
    PLAYER_X=100
    PLAYER_Y=300
    ENEMY_X=600
    ENEMY_Y=50
    FONT_HEIGHT=UC.default_font_pixel_height

    def __init__(self,player,enemy,renderer,music_mixer,sound_mixer):
        self.__renderer=renderer    #Handles rendering sprites to pycharm
        self.__player=player    #Player
        self.__enemy:Computer=enemy #Enemy
        self.__background=Background(0, 0, UC.screen_width, UC.screen_height)   #Background
        self.__animation_layer=Overlay(0,0,UC.screen_width,UC.screen_height)    #Special effects layer
        self.__clock=pygame.time.Clock()    #Timing handler
        self.__music_mixer=music_mixer  #Music player
        self.__sound_mixer=sound_mixer  #Sound Effect player
        self.__animator=BattleAnimator(sound_mixer) #Handles animating effects. Sound effects passed in

        self.__fps=30  #Controls game speed (Frames per second)
        self.__intro_started=False  #Controls the intro starting
        self.__playing_end_music=False  #Victory music check

        self.__running=False    #Controls main battle loop

        #Initialize game objects:
        self.__player_menu=None #player menu
        self.__message_box=None #Text at the bottom
        self.__messenger=None   #Handles sending text to the message box
        self.__enemy_stat_box=None  #Displays enemy hp/mp
        self.__player_stat_box=None #Displays player hp/mp
        self.__help_box=None    #Help text at the top of the screen
        self.__previous_screen=None #Surface containing the last screen, used for animation

        #Handles game turns:
        self.__turn_system= TurnSystem(player, enemy, self.__messenger,self.__animator)

        self.__menu_list=[]   #List of menu windows this is set in set_up_interface

        #Menu Variables:
        self.__target_menu=BattleMenu(self.DEFAULT_TARGET_MENU_X, self.DEFAULT_TARGET_MENU_Y, 100, 100)
        self.__target_menu.set_visible(False)
        self.__menu_tree=[] #Keeps track of the menu hierarchy while exploring
        self.__queued_action = None #Stores the function for the action while the user is selecting a target

        #These list all the interactive objects on screen to allow user to choose to point their action
        self.__enemy_dict=dict()    #List of enemies
        self.__team_dict=dict() #List of team members, not including player
        self.__active_dict=dict()   #List of all players on the field
        self.__self_dict=dict() #Just self
        self.__allies_dict=dict()
        self.__entire_party=dict()

        #Target dictionary. Menu references this to display available targets for a selected action:
        self.__target_dictionary={
            "enemies": self.__enemy_dict,
            "teammates": self.__team_dict,
            "active": self.__active_dict,
            "self": self.__self_dict,
            "party": {"Entire Team": self.__player},
            "allies": self.__team_dict
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
        #Player and enemy stat boxes
        self.__player_stat_box = StatBox(self.__player, 0, 175, 400, 125)
        self.__enemy_stat_box = StatBox(self.__enemy, 624, 350, 400, 125)

        #Text box and menu at the bottom:
        self.__message_box = InfoBox(0, 568, 680, 200, "", 5, (1, 1, 1))
        self.__player_menu = BattleMenu(681, 568, 347, 200, self.__player.get_menu_dictionary())

        #Menu lists and help box
        self.__menu_list = [self.__player_menu, self.__target_menu]  #Two menu boxes for displaying options
        self.__help_box=HelpBox(1,1,1000,40)

        #Set messengers for text delivery:
        self.__messenger = Messenger(self.__message_box, self.__sound_mixer)
        self.__player.set_messenger(self.__messenger)
        self.__enemy.set_messenger(self.__messenger)
        self.__turn_system.set_messenger(self.__messenger)

        #Set animation handler
        self.__enemy.set_animator(self.__animator)

        #Dictionary of objects for reference by the animator:
        self.__animator.update_object_dictionary({
            "enemy_stat_box":self.__enemy_stat_box,
            "player_stat_box": self.__player_stat_box,
            "player_menu_box": self.__player_menu,
            "message_box": self.__message_box,
            "messenger":self.__messenger,
            "player":self.__player,
            "enemy": self.__enemy,
            "background":self.__background,
            "animation_layer":self.__animation_layer,
            "help_box":self.__help_box
        })

    # =======================================================================================================
    def set_background(self, image=None):
        """
        Set the __background image
        :return:
        """
        #There are some magic numbers here specific to the background used.
        #In the future make this more dynamic

        back_width=2067 #UC.screen_width*1.1
        back_height=1162 #UC.screen_height
        x_offset=(back_width-UC.screen_width)/4
        y_offset=(back_height-UC.screen_height)/2
        #Offset background image to be able to scroll in animation:
        self.__background = Background(-x_offset, -y_offset, back_width, back_height,image)

    # =======================================================================================================
    def __set_positions(self):
        """
        Initializes starting positions.
        Animation handler uses these to know where to put objects after intro animation
        """
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
        self.__allies_dict= self.__list_team_including_self()
        self.__entire_party=self.__list_group_as_one()
        self.__target_dictionary={
            "enemies": self.__enemy_dict,
            "teammates": self.__team_dict,
            "active": self.__active_dict,
            "self": self.__self_dict,
            "party": self.__entire_party,
            "allies": self.__allies_dict
        }
    # =======================================================================================================
    def __list_group_as_one(self):
        """
        Create an object that represents the team as a whole
        """
        td=dict()
        td["Entire Party"] = {"owner": self.__player, "receiver": self.__player}
        return td

    # =======================================================================================================
    def __list_team_including_self(self):
        """
        Create a list of all team members and current character
        """
        td=dict()
        for teammate in self.__player.get_team().values():
            td[teammate.get_name()] = {"owner": self.__player, "receiver": teammate}
        return td

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
        renderer.add_to_layer(self.__help_box,2)
        renderer.add_to_layer(self.__message_box, 2)
        renderer.add_to_layer(self.__player_menu, 3)
        renderer.add_to_layer(self.__target_menu, 3)
        renderer.add_to_layer(self.__animation_layer,4)

    # =======================================================================================================
    def set_previous_screen(self,sprite):
        """
        Save the previous screen to show in intro animation
        :param sprite: Sprite object from the previous screen
        """
        self.__previous_screen=sprite

    def execute_menu(self,name):
        """
        Carries out an action when user selects an item from the battle menu
        :param name: A dictionary containing either another dictionary (sub menu) or Object (target)
        :return:
        """
        items={"":""}
        self.__target_menu.set_current_selection_number(0)  #Reset the menu pointer to 0
        #Looks for specific markers in the dictionary:
        #   "target" tells the algorithm to store the action function and wait for a target to be selected
        #   "menu" tells it that the next values are part of a sub menu
        #   Otherwise it looks for an object to direct the action to
        if isinstance(name,dict):
            if "target" in name:
                #Get the appropriate menu for the type of target required by the action:
                items=self.__target_dictionary[name["target"]]
                #Queue the action function with a reference name:
                self.__queued_action={"name": name["name"], "function": name["function"]}

                #Open the side menu:
                self.__target_menu.set_position(500, 500)
                self.__target_menu.update_menu(items, 300, len(items) * self.FONT_HEIGHT + 10)
                self.__target_menu.set_visible(True)

            elif "menu" in name:
                #Get the sub menu dictionary:
                items=name["menu"]

                #Open the side menu and update the items inside
                self.__target_menu.update_menu(items, 300, len(items) * self.FONT_HEIGHT + 10)
                self.__target_menu.set_visible(True)

            else:
                #Clear the menu tree, returning to main menu:
                self.__menu_tree.clear()
                self.__target_menu.set_visible(False) #Hide menu

                #Evaluate statuses of non-active team members:
                for team_member in self.__team_dict.values():
                    TurnSystem.evaluate_status_effects(team_member["receiver"], False)

                #Execute action from in the dictionary:
                self.__turn_system.perform_action(self.__player, self.__queued_action, name)

                # Switch to __enemy turn
                self.__turn_system.set_player_turn(False)

        #Display tooltip at the top:
        self.show_description(self.__menu_list[self.__target_menu.get_visible()])


    # =======================================================================================================
    def listen_for_input_and_events(self,event_list):
        """
        Listens for key presses from the user
        :param event_list: List of key/window events passed by pygame
        :return:
        """

        #Get player turn and animation status:
        player_turn = self.__turn_system.get_player_turn()
        animating=self.__animator.get_animating_status()
        #Current menu:
        menu=self.__menu_list[self.__target_menu.get_visible()]

        for event in event_list:
            if event.type == btn.QUIT:  # Click close
                self.__running = False  # end loop

            elif event.type == UC.MUSIC_EVENT_END:  # Music ends
                self.__music_mixer.repeat_music()  # Repeat battle music

                if self.__turn_system.get_battle_status() == "victory":  # Check for victory status
                    pass
                    # self.__running=False

            if event.type == KEYDOWN:

                #These are always listed for:
                if event.key== btn.K_ESCAPE:    #Escape key
                    self.__running = False  #end loop



                #These are only listened for when is player turn and no animations occurring:
                if player_turn and not animating and self.__turn_system.get_battle_status()=="ongoing":

                    #Switch Case:
                    match event.key:
                        case btn.K_KP_PLUS: #Numpad +
                            self.__fps+=10  #Speed up game
                            print(self.__fps)

                        case btn.K_KP_MINUS:    #Numpad -
                            self.__fps-=10  #Slow down game
                            print(self.__fps)
                        case btn.K_1:
                            self.__player.get_current_character().set_curr_hp(1)
                        case btn.K_LEFT:    #Left key
                            pass

                        case btn.K_RIGHT:   #Right key
                            pass

                        case btn.K_UP:  #Up key
                            #Go to previous menu item and display text
                            menu.prev_menu_item()
                            self.show_description(menu)

                        case btn.K_DOWN:    #Down key
                            #Go to next menu item and display text
                            menu.next_menu_item()
                            self.show_description(menu)

                        case btn.K_BACKSPACE:   #Backspace key
                            #Go down one menu level
                            self.__queued_action=None
                            #Pops the last menu from the menu tree
                            if len(self.__menu_tree)>0:
                                self.__menu_tree.pop()

                            #Hide side menu if base menu reached
                            if len(self.__menu_tree)==0:
                                self.__target_menu.set_visible(False)
                            else:
                                self.execute_menu(self.__menu_tree[-1])

                            #Display help text
                            menu = self.__menu_list[self.__target_menu.get_visible()]
                            self.show_description(menu)

                        case btn.K_RETURN:  #Enter/Return Key
                            name=0
                            #Get menu dictionary
                            self.__player.get_menu_dictionary()

                            #If base menu, get base menu item, else get side menu item
                            if len(self.__menu_tree)==0:
                                name=self.__menu_list[0].get_current_selection()
                            else:
                                name = self.__menu_list[1].get_current_selection()

                            #Add new menu to the stack and execute
                            self.__menu_tree.append(name)
                            self.execute_menu(name)



    # =======================================================================================================
    def perform_updates(self):
        """
        Updates that happen every cycle
        :return:
        """
        #Help box only visible when player can access menu:
        self.__help_box.set_visible(self.__turn_system.get_player_turn() and  not self.__animator.get_animating_status())

        #Ensure selection menus are up to date:
        self.update_dictionaries()

        #Keep menus updated
        self.__player_menu.update_menu(self.__player.get_menu_dictionary())

        #Stream text to message box
        self.__messenger.stream_text()

        #Perform animations:
        self.__animator.animate_list()

        #Update enemy stats and player stats after animations:
        if not self.__animator.get_animating_status() or self.__enemy_stat_box.get_animating():
            self.__enemy_stat_box.update_stats()

        if not self.__animator.get_animating_status() or self.__player_stat_box.get_animating():
            self.__player_stat_box.update_stats()

        #Check for win and loss conditions
        self.__turn_system.check_loss_conditions()
        if self.__turn_system.check_win_conditions():
            pass
    # =======================================================================================================
    def show_description(self, on_menu):
        """
        Update help box at top of screen
        """
        m_dict=on_menu.get_current_selection()
        if "description" in m_dict:
            self.__help_box.write_in_box(m_dict["description"])
        else:
            self.__help_box.write_in_box("")

    # =======================================================================================================
    def show_battle_intro(self):
        """
        Do introductory battle animations
        """
        #Create a surface to start:
        surf=Sprite(0,0,UC.screen_width,UC.screen_height,None,(127,127,127),(1,0,0))

        #Draw previous screen onto the new surface
        if self.__previous_screen is not None:
            surf.draw_on_surface(self.__previous_screen.get_surface(),0,0,True)

        #Create a series of animation frames for intro with previous screen and battle screen
        intro_effect=Effect(
            0,0,UC.screen_width,UC.screen_height,
            Effect.generate_battle_transition(surf.get_surface(),9,10)
        )
        #Pass animation frames into animator and queue animations
        self.__animator.pause_and_animate({"action":"Screen_Transition","subject": intro_effect})
        self.__animator.pause_and_animate({"action":"Intro","subject":"errbody"})

    # =======================================================================================================
    def set_enemy_battle_stats(self):
        """
        Battle stats are derived from base stats
        Ex: STR determines ATK and DEF, while INT determines SKL_ATK,POT, SKL_DEF, and RES
        Initializes all stats at the beginning of battle
        """
        for teammate in self.__enemy.get_team().values():
            teammate.calculate_start_battle_stats()
    # =======================================================================================================
    def set_player_battle_stats(self):
        """
        Battle stats are derived from base stats
        Ex: STR determines ATK and DEF, while INT determines SKL_ATK,POT, SKL_DEF, and RES
        Initializes all stats at the beginning of battle
        """
        for teammate in self.__player.get_team().values():
            teammate.calculate_start_battle_stats()
    # =======================================================================================================
    def change_music(self,new_song,start=0,repeat_time=-1):
        """
        Calls on mixer to play new song
        :param new_song: Song file to play
        :param start: Start time of music
        :param repeat_time: Time signature to loop on music end
        """
        self.__music_mixer.stop_music()
        self.__music_mixer.play_music(new_song,start,repeat_time)

    # =======================================================================================================
    def start(self):
        """
        Main Battle loop
        :return:
        """
        #Turn on loop
        self.__running=True
        #Show intro scene
        # self.show_battle_intro()
        #Start music
        self.__music_mixer.play_music(start=0,repeat_time=13.19)
        #Initialize player and enemy stats:
        self.set_player_battle_stats()
        self.set_enemy_battle_stats()

        #Begin main loop:
        while self.__running:
            #Get player turn and animation status
            player_turn=self.__turn_system.get_player_turn()
            animating=self.__animator.get_animating_status()

            #Perform battle updates:
            self.perform_updates()

            #Get events:
            game_events=pygame.event.get()

            #Take action based on events and user input:
            self.listen_for_input_and_events(game_events)

            #If computer turn, let computer take action
            if not player_turn and not animating:
                self.__turn_system.cpu_perform_action()

            #Render all sprites and layers
            self.__renderer.render_all()
            self.__renderer.flip_screen()

            #Keep fps constant:
            self.__clock.tick(self.__fps)

            #Check for end of battle:
            if self.__turn_system.get_battle_status()=="victory" and not animating and player_turn and not self.__playing_end_music:
               self.change_music(UC.victory_music)
               self.__playing_end_music=True

            if self.__turn_system.get_battle_status()=="loss" and not animating and player_turn and not self.__playing_end_music:
               self.change_music(UC.failure_music)
               self.__playing_end_music=True





