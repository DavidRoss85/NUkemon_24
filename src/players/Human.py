from src.globals.UC import UC

from src.units.Character import Character
from src.units.Team import Team

class Player(Team):
    def __init__(self):
        super().__init__()
        self.__y = 0
        self.__x = 0
        self.move_list=[]
        self.__move_dict=dict()
        self.__character_moves=[]
        self.__visible=True




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
        # self.move_list= self.current_character.get_move_list() + self.get_menu_dictionary()
        self.move_list=list(self.__move_dict.keys())
        return self.__move_dict

    def set_visible(self,value:bool=True):
        self.__visible=value

    def get_visible(self):
        return self.__visible

##This function needs an additional part to choose the player target or use sub menus:
    def execute_menu_item(self,item,menu_func):
        print(item)
        menu_func(item)
        # self.__move_dict[item](target)

    #--TESTING:
    def test_set_target(self,target):
        # For testing... Remove later:
        self.get_current_character().set_target(target)