import copy
from random import randint

from src.globals.balance import VARIABILITY
from src.units.Character import Character
from src.units.SkillClasses import Skill


class LazyStudent(Character):
    def __init__(self, name, level, hp, mp, strength, intel, sprite, x=0, y=0):
        super().__init__(name, level, hp, mp, strength, intel, sprite, x, y)
        self.set_profession("Lazy Student")
        self.__profession_move=Skill("Sleep in Class", ["heal"], 1, 10, ["asleep"], 1, 3)
        self.get_condition().immunities = []
        self.__lazy_move_dict = {
            "Skill": {
                "menu": {
                    "Sleep in Class": {
                        "name": "Sleep in Class", "target": "self", "function": self.sleep_in_class
                    }
                }
            }
        }

        self.update_move_dictionary(self.__lazy_move_dict)

    def sleep_in_class(self,target):
        # stats=self.get_battle_stats()
        # target.set_curr_hp(target.get_curr_hp()+0)
        # current_move=copy.deepcopy(self.__profession_move)
        # self.set_curr_mp(self.get_curr_mp()-current_move.cost)
        # current_move.dmg= (stats.sk_atk + randint(0,(stats.sk_atk*VARIABILITY))) * current_move.dmg
        # current_move.potency+=stats.potency + randint(0,(stats.potency*VARIABILITY))
        # target.receive_attack(current_move)
        self.perform_special_move(self,target,self.__profession_move)
        return self