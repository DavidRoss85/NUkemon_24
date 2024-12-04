import copy
from random import randint

from src.globals.balance import VARIABILITY
from src.units.Character import Character
from src.units.SkillClasses import Skill


class Husky(Character):
    def __init__(self,name,level,hp,mp,strength,intel,sprite,x=0,y=0):
        super().__init__(name,level,hp,mp,strength,intel,sprite,x,y)
        self.set_profession("Husky")
        self.get_condition().immunities=["confused"]
        self.__profession_move = Skill("Growl", ["mental"], 0, 10, ["afraid"], 1, 3)
        self.__husky_move_dict={
            "Skill":{
                "menu":{
                    "Growl": {
                        "name": "Growl", "target": "enemies", "function":self.use_growl
                    }
                }
            }
        }

        self.update_move_dictionary(self.__husky_move_dict)




    def use_growl(self,target):
        self.deliver_message(f"{self.get_name()} uses {self.__profession_move.name}...\n ")
        current_move = copy.deepcopy(self.__profession_move)
        self.set_curr_mp(self.get_curr_mp() - current_move.cost)
        current_move.potency += self.get_battle_stats().potency + randint(0, (
                    self.get_battle_stats().potency * VARIABILITY))
        target.receive_attack(current_move)