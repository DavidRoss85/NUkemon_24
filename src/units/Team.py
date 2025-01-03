from src.systems.TurnSystem import TurnSystem
from src.units.Character import Character

class Team:
    """Teams contain lists of multiple characters and form the basis for player and enemy objects"""
    def __init__(self):
        self.__y = 0    #x coord
        self.__x = 0    #y coord
        self.__move_dict=dict() #Move dictionary
        self.__visible=True #Toggle visibility

        self.__team = dict()    #Dictionary of team members
        self.__expired_team=dict()  #KO'd team members
        self.__current_character:Character = None   #First team member
        self.__frozen_frame=False   #Used for animation to stop changing current sprite
        self.sprite_frame=None  #Holds the current sprite information

        #Menu dictionary to switch characters to the menu
        self.__menu_options={
            "Switch": {
                "name": "Switch",
                "target": "teammates",
                "function":self.change_character,
                "description": "Change characters"
            },
            "Pass": {
                "name":"Pass",
                "target": "self",
                "function": self.nothing_func,
                "description": "Do nothing this round"
            }
        }
        #Empty menu dictionary when there are no characters left to switch to:
        self.__no_team_options={
            "Pass": {
                "name": "Pass",
                "target": "self",
                "function": self.nothing_func,
                "description": "Do nothing this round"
            }
        }

        #Set messenger for receiving text
        self.__messanger=None



    def get_x(self):
        """
        :return: x coord of current character
        """
        self.__x=self.get_current_character().get_x()
        return self.__x

    def get_y(self):
        """
        :return: y coord of current character
        """
        self.__y=self.get_current_character().get_y()
        return self.__y

    def set_x(self,x):
        """
        Set x coord of current character
        :param x: x coord
        """
        self.__x=x
        self.get_current_character().set_x(x)

    def set_y(self,y):
        """
        Set y coord of current character
        :param y: y coord
        """
        self.__y=y
        self.get_current_character().set_y(y)

    def get_menu_dictionary(self):
        """
        Combine all menu options available into one and return
        """
        #Clear current move dictionary:
        self.__move_dict=dict()

        #Add moves for current character:
        self.__move_dict.update(self.get_current_character().get_move_dictionary())

        #Add team moves:
        self.__move_dict.update(self.get_team_dictionary())

        #Append status if move is blocked:
        #Get allowed moves by evaluating the player's status:
        allowed=TurnSystem.evaluate_status_effects(self.__current_character)["allowed"]


        if 'all' not in allowed:
            for key in self.__move_dict:
                #Block all moves that are not in the allowed list:
                if key not in allowed:
                    self.__move_dict[key].update({"status":"blocked"})

                #Unblock others:
                elif "status" in self.__move_dict[key]:
                    self.__move_dict[key].update({"status":"allowed"})

        else:
            #If all items allowed re-enable everything:
            for key in self.__move_dict:
                self.__move_dict[key].update({"status":"allowed"})

        #Return updated dictionary
        return self.__move_dict.copy()

    def set_visible(self,value:bool=True):
        """
        Toggle visibility
        :param value: True/False
        """
        self.__visible=value

    def get_visible(self):
        """
        :return: visibility
        """
        return self.__visible

    def freeze_frame(self):
        """
        Setting freeze-frame prevents the current sprite from updating (Used for switching animations)
        """
        self.__frozen_frame=True

    def unfreeze_frame(self):
        """
        Resumes sprite updates
        """
        self.__frozen_frame=False

    def get_name(self):
        """
        :return: Name of current character
        """
        return self.__current_character.get_name()

    def get_team(self):
        """
        :return: current team dictionary
        """
        return self.__team

    def get_graveyard(self):
        """
        :return: expired team dictionary
        """
        return self.__expired_team

    def set_team(self,team_list:list):
        """
        Sets the current team to the members in the list.
        :param team_list: List of character objects
        """
        #Clear current team list:
        self.__team=dict()
        #Add members on list to dictionary
        for teammate in team_list:
            self.add_team_member(teammate)

    def receive_attack(self,attack):
        print(f"Team.receive_attack: Team received attack")
        for character in self.__team.values():
            character.receive_attack(attack)

    def send_to_graveyard(self,team_member):
        """
        Knocked out characters go to the graveyard.
        :param team_member: Character object that is being sent to graveyard
        """
        #Check if in team dictionary:
        if  team_member.get_name() in self.__team:
            #Add to graveyard dictionary:
            self.__expired_team[team_member.get_name()]=team_member
            #Remove from team dictionary:
            del self.__team[team_member.get_name()]
            #Announce player KO:
            self.__deliver_message(f"{self.__current_character.get_name()} has lost consciousness!\n ")
            #Force change of characters
            self.change_character(self.__team[next(iter(self.__team))])
            return self


    def add_team_member(self, team_member):
        """
        Add a player to the team roster
        :param team_member: Character Object
        """
        #Set current owner:
        team_member.set_owner(self)
        #Add to dictionary
        self.__team[team_member.get_name()] = team_member
        #Set to team lead if noone else in team
        if self.__current_character is None:
            self.change_character(team_member)


    def change_character(self,target):
        """
        Switch to another member of your team
        :param target: Character Object to switch to
        """
        #Check if character in team:
        if target.get_name() in self.__team:

            #Announce switch
            if self.__current_character is not None:
                self.__deliver_message(f"{target.get_name()} takes over for "
                                       f"{self.__current_character.get_name()}\n ")

            #Set current character to target
            self.__current_character = self.__team[target.get_name()]
            #update the menu options
            self.get_menu_dictionary()
            #Return the owner of the character
            return self

    def get_current_character(self):
        """
        :return: Current character
        """
        return self.__current_character

    def get_sprite(self):
        """
        Return the current sprite object, but only update if frozen frame is off
        :return: Sprite
        """
        #Allows the program to freeze the current frame
        if not self.__frozen_frame:
            self.sprite_frame= self.__current_character.get_sprite()

        return self.sprite_frame

    def get_curr_hp(self):
        """
        :return: current character hp
        """
        return self.__current_character.get_curr_hp()

    def get_team_dictionary(self):
        """
        :return: menu options for teams
        """
        #Only return an option to switch if there is more than one person on the team:
        if len(self.__team)>1:
            return self.__menu_options
        else:
            return self.__no_team_options

    def set_curr_hp(self, value):
        """
        Set current character hp
        :param value: Integer value
        """
        self.__current_character.set_curr_hp(value)

    def set_messenger(self,messenger):
        """
        Set messenger for current character and team members
        :param messenger: Messenger Object
        """
        self.__messanger=messenger
        for team_member in self.__team.values():
            team_member.set_messenger(messenger)

    def __deliver_message(self,message):
        """
        Send a message to the text box to be streamed
        :param message:String of text to be displayed
        """
        self.__messanger.process_message(message)

    def nothing_func(self,args=None):
        return self

