
from src.units.Character import Character
from src.units.SkillClasses import Skill


class CSProfessor(Character):
    """Professor with Computer science related Skills"""
    def __init__(self,name,level,hp,mp,strength,intel,sprite,x=0,y=0):
        super().__init__(name,level,hp,mp,strength,intel,sprite,x,y)
        self.set_profession("CS Professor")
        self.get_condition().immunities=["confused"]
        self.__profession_move=Skill("Algorithms", ["mental"], 0, 10, ["stronger","smarter"], 1, 4)
        self.__profession_dict = {
            "Skill": {
                "description": "Use a special ability",
                "menu":{
                    "Algorithms": {
                        "name": "Algorithms",
                        "target": "team",
                        "function": self.use_algorithms,
                        "description": "Raises the targets intellect and strength for 3 turns"
                    }
                }
            }
        }

        self.update_move_dictionary(self.__profession_dict)

    def use_algorithms(self,target=None):
        if "confused" in self.get_battle_effects():
            self.deliver_message(f"{self.get_name()} tried to use Algorithms, but {self.get_name()} is confused.\n ")
            return self
        self.deliver_message(f"{self.get_name()} used Algorithms!\n ")
        self.perform_special_move(self,target,self.__profession_move)
        return self