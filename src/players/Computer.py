from random import randint

from src.globals.UC import UC
from src.systems.Animator import Animator
from src.units.Team import Team

class Computer(Team):
    def __init__(self):
        super().__init__()
        self.__y = 0
        self.__x = 0
        self.move_list=[]
        self.__move_dict=dict()
        self.__character_moves=[]
        self.__visible=True
        self.animator=None




    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def set_x(self,x):
        self.__x=x

    def set_y(self,y):
        self.__y=y

    def get_menu_dictionary(self):
        # self.get_current_character().update_move_dictionary(self.get_menu_dictionary())
        self.__move_dict.update(self.get_current_character().get_move_dictionary())
        self.__move_dict.update(self.get_team_dictionary())
        # self.move_list= self.__current_character.get_move_list() + self.get_menu_dictionary()
        self.move_list=list(self.__move_dict.keys())
        return self.__move_dict

    def set_visible(self,value:bool=True):
        self.__visible=value

    def get_visible(self):
        return self.__visible

    def execute_move(self,player):
        self.get_menu_dictionary()

        #<<CPU AI LOGIC GOES HERE>>
        num=randint(1,10)
        # print(player)
        if num>5:
            self.__move_dict["Attack"]["function"](player.get_current_character())
            self.animator.pause_and_animate({"subject":self,"action":"Attack"})
            self.animator.pause_and_animate({"object": player, "action": "Attack"})
        else:
            self.__move_dict["Defend"]["function"](self.get_current_character())

        return True
