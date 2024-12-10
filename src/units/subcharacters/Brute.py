from src.units.SkillClasses import Skill
from src.units.Character import Character


class Brute(Character):
    """Strong Character favoring physical attacks"""
    def __init__(self, name, level, hp, mp, strength, intel, sprite, x=0, y=0):
        super().__init__(name, level, hp, mp, strength, intel, sprite, x, y)
        self.set_profession("Brute")
        self.__profession_move=Skill("Combo Attack", ["physical"], 2, 10, ["injured"], 2, 3)
        self.get_condition().immunities = ["injured"]
        self.__profession_dict = {
            "Skill": {
                "description": "Use a special ability",
                "menu": {
                    "Combo Attack": {
                        "name": "Combo Attack",
                        "target": "enemies",
                        "function": self.combo_attack,
                        "description": "Launches an all out attack against the opponent."
                    }
                }
            }
        }

        self.update_move_dictionary(self.__profession_dict)

    def combo_attack(self,target):
        if "confused" in self.get_battle_effects():
            self.deliver_message(f"{self.get_name()} tried to use Combo Attack, but {self.get_name()} is confused.\n ")
            return
        # self.get_battle_stats().potency=100
        self.deliver_message(f"{self.get_name()} used Combo Attack!\n ")
        self.perform_special_move(self,target,self.__profession_move)
        return self