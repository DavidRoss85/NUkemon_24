
from src.units.Character import Character
from src.units.SkillClasses import Skill


class CSProfessor(Character):
    """Professor with Computer science related Skills"""
    def __init__(self,name,level,hp,mp,strength,intel,sprite,x=0,y=0):
        super().__init__(name,level,hp,mp,strength,intel,sprite,x,y)
        self.set_profession("CS Professor")
        self.get_condition().immunities=["confused","lagging", "lagging AF"]
        self.__algorithms_move=Skill("Algorithms", ["mental"], 0, 10, ["stronger", "smarter"], 5, 4)
        self.__n2_move=Skill("ON2", ["mental"], 0, 10, ["lagging"], 2, 11)
        self.__n3_move=Skill("ON3", ["mental"], 0, 20, ["laggy AF"], 2, 10)
        self.__profession_dict = {
            "Skill": {
                "description": "Use a special ability",
                "menu":{
                    "Algorithms": {
                        "name": "Algorithms",
                        "target": "allies",
                        "function": self.use_algorithms,
                        "description": "Raises the targets intellect and strength for 3 turns"
                    },
                    "Big O Notation": {
                        "description": "Use time complexity to gain an advantage",
                        "menu": {
                            "n^2":{
                                "name": "n2",
                                "target": "enemies",
                                "function": self.use_n2,
                                "description": "Target can only attack ever other turn"
                            },
                            "n^3":{
                                "name": "n3",
                                "target": "enemies",
                                "function": self.use_n3,
                                "description": "Target can only attack every third turn"
                            }

                        }
                    }
                }
            }
        }
        self.set_atk_move_name("a Hard Drive")

        self.update_move_dictionary(self.__profession_dict)

    def use_algorithms(self,target=None):
        if "confused" in self.get_battle_effects():
            self.deliver_message(f"{self.get_name()} tried to use Algorithms, but {self.get_name()} is confused.\n ")
            return self
        self.deliver_message(f"{self.get_name()} used Algorithms!\n ")
        self.perform_special_move(self, target, self.__algorithms_move)
        return self

    def use_n2(self,target=None):

        self.deliver_message(f"{self.get_name()} used O ( n^2 )!\n ")
        self.perform_special_move(self, target, self.__n2_move)
        return target.get_owner()

    def use_n3(self,target=None):

        self.deliver_message(f"{self.get_name()} used O ( n^3 )!\n ")
        self.perform_special_move(self, target, self.__n3_move)
        return target.get_owner()