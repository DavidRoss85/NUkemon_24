
from src.units.Character import Character
from src.units.SkillClasses import Skill


class MathProfessor(Character):
    def __init__(self,name,level,hp,mp,strength,intel,sprite,x=0,y=0):
        super().__init__(name,level,hp,mp,strength,intel,sprite,x,y)
        self.set_profession("Math professor")
        self.get_condition().immunities=["confused"]
        self.__profession_move=Skill("Discreet Math", ["mental"], 0, 10, ["confused"], 1, 3)
        self.__math_professor_move_dict = {
            "Skill": {
                "menu":{
                    "Discreet Math": {
                        "name": "Discreet Math", "target": "enemies", "function": self.use_discreet_math
                    }
                }
            }
        }

        self.update_move_dictionary(self.__math_professor_move_dict)

    def use_discreet_math(self,target=None):
        if "confused" in self.get_battle_effects():
            self.deliver_message(f"{self.get_name()} tried to use Discreet Math, but {self.get_name()} is confused.\n ")
            return

        self.perform_special_move(self,target,self.__profession_move)