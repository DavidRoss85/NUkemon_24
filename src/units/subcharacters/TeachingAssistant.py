import copy
from random import randint

from src.globals.balance import VARIABILITY
from src.units.Character import Character
from src.units.SkillClasses import Skill


class TeachingAssistant(Character):
    """Teaching Assistant Character"""
    def __init__(self, name, level, hp, mp, strength, intel, sprite, x=0, y=0):
        super().__init__(name, level, hp, mp, strength, intel, sprite, x, y)
        self.set_profession("TA")
        self.get_condition().immunities = []
        self.__profession_move = Skill("Shoo", ["mental"], 0, 10, ["disheartened"], 1, 3)
        self.__profession_dict = {
            "Skill": {
                "description": "Use a special ability",
                "menu": {
                    "Shoo": {
                        "name": "Shoo",
                        "target": "enemies",
                        "function": self.shoo_away,
                        "description": "Shoos away the target, making them feel bad"
                    }
                }
            }
        }

        self.update_move_dictionary(self.__profession_dict)

    def shoo_away(self,target):
        self.deliver_message(f"{self.get_name()} used Shoo!\n 'Ew! Get away from me!'\n ")
        self.perform_special_move(self,target,self.__profession_move)