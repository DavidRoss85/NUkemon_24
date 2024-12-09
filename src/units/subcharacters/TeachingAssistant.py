import copy
from random import randint

from src.globals.balance import VARIABILITY
from src.units.Character import Character
from src.units.SkillClasses import Skill


class TeachingAssistant(Character):
    def __init__(self, name, level, hp, mp, strength, intel, sprite, x=0, y=0):
        super().__init__(name, level, hp, mp, strength, intel, sprite, x, y)
        self.set_profession("Husky")
        self.get_condition().immunities = []
        self.__profession_move = Skill("Shoo", ["mental"], 0, 10, ["disheartened"], 1, 3)
        self.__t_a_move_dict = {
            "Skill": {
                "menu": {
                    "Shoo": {
                        "name": "Shoo",
                        "target": "enemies",
                        "function": self.stub_func,
                        "description": "Shoos away the target, making them feel bad"
                    }
                }
            }
        }

        self.update_move_dictionary(self.__t_a_move_dict)

    def stub_func(self,target):

        self.perform_special_move(self,target,self.__profession_move)