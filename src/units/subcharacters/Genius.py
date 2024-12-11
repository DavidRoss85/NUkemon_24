
from src.units.SkillClasses import Skill
from src.units.Character import Character


class Genius(Character):
    """Highly intelligent student"""
    def __init__(self, name, level, hp, mp, strength, intel, sprite, x=0, y=0):
        super().__init__(name, level, hp, mp, strength, intel, sprite, x, y)
        self.set_profession("Genius")
        self.__profession_move=Skill("Explain", ["mental","remedy"], 0, 5, ["un-confused"], 1, 1)
        self.__profession_move2=Skill("Early HW",["mental"],1.5,0,["overwhelmed"],10,2)
        self.get_condition().immunities = ["confused"]
        self.__profession_dict = {
            "Skill": {
                "description": "Use a special ability",
                "menu": {
                    "Explain": {
                        "name": "Explain",
                        "target": "teammates",
                        "function": self.explain,
                        "description": "Removes confusion from one teammate"
                    },
                    "Turn in H/W Early": {
                        "name": "Early HW",
                        "target": "enemies",
                        "function": self.early_homework,
                        "description": "Use all of your remaining MP to overwhelm the target with assignments. (Causes damage and paralysis)"
                    }
                }
            }
        }

        self.update_move_dictionary(self.__profession_dict)

    def explain(self,target):
        self.deliver_message(f"{self.get_name()} used Explain!\n ")
        self.perform_special_move(self,target,self.__profession_move)
        return self

    def early_homework(self,target):
        self.deliver_message(f"{self.get_name()} Turned in all projects and assignments ahead of time!\n ")
        self.__profession_move2.cost=self.get_battle_stats().mp
        self.perform_special_move(self, target, self.__profession_move2)
        return target.get_owner()