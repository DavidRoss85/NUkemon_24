from src.globals.UC import UC

from src.Units.Character import Character

class Team:
    def __init__(self):
        self.__team = dict()
        self.current_character:Character = None

    def add_team_member(self, team_member):
        self.__team[team_member.get_name()] = team_member
        if self.current_character is None:
            self.change_character(team_member.get_name())

    def change_character(self, name):
        if name in self.__team:
            self.current_character = self.__team[name]

    def get_current_character(self):
        return self.current_character

    def get_sprite(self):
        return self.current_character.get_sprite()

    def get_curr_hp(self):
        return self.current_character.get_curr_hp()

    def set_curr_hp(self, value):
        self.current_character.set_curr_hp(value)