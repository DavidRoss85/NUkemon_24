from src.globals.UC import UC

from src.Units.Character import Character

class Team:
    def __init__(self):
        self.__team = dict()
        self.current_character:Character = None
        self.__menu_options={
            "Summon": self.change_character
        }
        self.__switch_to="Mina"


    def add_team_member(self, team_member):
        self.__team[team_member.get_name()] = team_member
        if self.current_character is None:
            self.__switch_to=team_member.get_name()
            self.change_character()
            self.__switch_to="Mina"

    def change_character(self):
        if self.__switch_to in self.__team:
            self.current_character = self.__team[self.__switch_to]

    def get_current_character(self):
        return self.current_character

    def get_sprite(self):
        return self.current_character.get_sprite()

    def get_curr_hp(self):
        return self.current_character.get_curr_hp()

    def get_menu_dictionary(self):
        return self.__menu_options

    def set_curr_hp(self, value):
        self.current_character.set_curr_hp(value)