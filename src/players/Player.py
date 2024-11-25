from src.globals.UC import UC

from src.players.Character import Character


class Player:
    def __init__(self):
        self.move_list=[]
        self.__team = dict()
        self.current_character = None



    def update_move_list(self):
        self.move_list=self.current_character.get_move_list()

    def add_team_member(self,team_member):
        self.__team[team_member.get_name()]=team_member
        if self.current_character is None:
            self.change_character(team_member.get_name())

    def change_character(self,name):
        if name in self.__team:
            self.current_character=self.__team[name]

    def get_current_character(self):
        return self.current_character

    def get_sprite(self):
        return self.current_character.get_sprite()