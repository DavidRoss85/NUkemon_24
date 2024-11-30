from src.globals.UC import UC

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
        self.__x=self.get_current_character().get_x()
        return self.__x

    def get_y(self):
        self.__y=self.get_current_character().get_y()
        return self.__y

    def set_x(self,x):
        self.__x=x
        self.get_current_character().set_x(x)

    def set_y(self,y):
        self.__y=y
        self.get_current_character().set_y(y)

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

