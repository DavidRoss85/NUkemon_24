from src.globals.UC import UC

from src.Units.Character import Character

class Team:
    def __init__(self):
        self.__team = dict()
        self.current_character:Character = None
        self.__menu_options={
            "Switch": {"target": "team", "function":self.change_character},
            "Do Magic": {"menu": {
                    "fire": {"target": "enemies"},
                    "water":{"target": "enemies"},
                    "earth":{"target": "enemies"},
                }
            },
        }
        self.__messanger=None


    def get_team(self):
        return self.__team
    def add_team_member(self, team_member):
        self.__team[team_member.get_name()] = team_member

        if self.current_character is None:
            self.change_character(team_member)


    def change_character(self,target):
        if target.get_name() in self.__team:
            if self.current_character is not None:
                self.__deliver_message(f"{self.current_character.get_name()} "
                                   f"switches to {target.get_name()}\n ")

            self.current_character = self.__team[target.get_name()]

    def get_current_character(self):
        return self.current_character

    def get_sprite(self):
        return self.current_character.get_sprite()

    def get_curr_hp(self):
        return self.current_character.get_curr_hp()

    def get_team_dictionary(self):
        return self.__menu_options

    def set_curr_hp(self, value):
        self.current_character.set_curr_hp(value)

    def set_messenger(self,messenger):
        self.__messanger=messenger
        for team_member in self.__team.values():
            team_member.set_messenger(messenger)

    def __deliver_message(self,message):
        self.__messanger.process_message(message)