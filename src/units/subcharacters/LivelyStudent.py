
from src.units.SkillClasses import Skill
from src.units.Character import Character


class LivelyStudent(Character):
    """Student with lazy characteristics"""
    def __init__(self, name, level, hp, mp, strength, intel, sprite, x=0, y=0):
        super().__init__(name, level, hp, mp, strength, intel, sprite, x, y)
        self.set_profession("Lively Student")
        self.__profession_move=Skill("Excuses", ["mental"], 0, 10, ["asleep"], 2, 2)
        self.get_condition().immunities = ["alseep", "laggy AF"]
        self.__profession_dict = {
            "Skill": {
                "description": "Use a special ability",
                "menu": {
                    "Explain Myself": {
                        "name": "Explain Myself",
                        "target": "enemies",
                        "function": self.explain_myself,
                        "description": "Student tries desperately to explain their mistakes."
                    }
                }
            }
        }
        self.set_atk_move_name("a slap")
        self.update_move_dictionary(self.__profession_dict)

    def explain_myself(self,target):
        self.deliver_message(f"{self.get_name()} Tries to explain themself... \n ")
        self.perform_special_move(self,target,self.__profession_move)
        return self