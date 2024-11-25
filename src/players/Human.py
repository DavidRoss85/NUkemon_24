from src.globals.UC import UC

from src.Units.Character import Character
from src.Units.Team import Team

class Player(Team):
    def __init__(self):
        super().__init__()
        self.move_list=[]
        self.__visible=True

    def update_move_list(self):
        self.move_list=self.current_character.get_move_list()
        return self.move_list

    def set_visible(self,value:bool=True):
        self.__visible=value

    def get_visible(self):
        return self.__visible
