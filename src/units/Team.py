from src.globals.UC import UC

from src.units.Character import Character

class Team:
    def __init__(self):
        self.__team = dict()
        self.__current_character:Character = None
        self.__menu_options={
            "Switch": {"name": "Switch","target": "team", "function":self.change_character},
        }

        # "Do Magic": {"menu": {
        #     "fire": {"target": "enemies"},
        #     "water": {"target": "enemies"},
        #     "earth": {"target": "enemies"},
        # }
        # },
        self.__messanger=None


    def get_team(self):
        return self.__team

    def set_team(self,team_list:list):
        for teammate in team_list:
            self.add_team_member(teammate)

    def add_team_member(self, team_member):
        self.__team[team_member.get_name()] = team_member
        if self.__current_character is None:
            self.change_character(team_member)


    def change_character(self,target):
        if target.get_name() in self.__team:
            if self.__current_character is not None:
                self.__deliver_message(f"{self.__current_character.get_name()} "
                                   f"switches to {target.get_name()}\n ")

            self.__current_character = self.__team[target.get_name()]

    def get_current_character(self):
        return self.__current_character

    def get_sprite(self):
        return self.__current_character.get_sprite()

    def get_curr_hp(self):
        return self.__current_character.get_curr_hp()

    def get_team_dictionary(self):
        return self.__menu_options

    def set_curr_hp(self, value):
        self.__current_character.set_curr_hp(value)

    def set_messenger(self,messenger):
        self.__messanger=messenger
        for team_member in self.__team.values():
            team_member.set_messenger(messenger)

    def __deliver_message(self,message):
        self.__messanger.process_message(message)