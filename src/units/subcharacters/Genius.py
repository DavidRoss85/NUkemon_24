
from src.units.SkillClasses import Skill
from src.units.Character import Character


class Genius(Character):
    def __init__(self, name, level, hp, mp, strength, intel, sprite, x=0, y=0):
        super().__init__(name, level, hp, mp, strength, intel, sprite, x, y)
        self.set_profession("Genius")
        self.__profession_move=Skill("Explain", ["mental","remedy"], 0, 5, ["un-confused"], 1, 1)
        self.get_condition().immunities = ["confused"]
        self.__profession_dict = {
            "Skill": {
                "description": "Use a special ability",
                "menu": {
                    "Explain": {
                        "name": "Explain",
                        "target": "team",
                        "function": self.explain,
                        "description": "Removes confusion from one teammate"
                    }
                }
            }
        }

        self.update_move_dictionary(self.__profession_dict)

    def explain(self,target):
        self.deliver_message(f"{self.get_name()} used Explain!\n ")
        self.perform_special_move(self,target,self.__profession_move)
        return self