
from src.units.Character import Character
from src.units.SkillClasses import Skill


class Husky(Character):
    """NU Husky mascot"""
    def __init__(self,name,level,hp,mp,strength,intel,sprite,x=0,y=0):
        super().__init__(name,level,hp,mp,strength,intel,sprite,x,y)
        self.set_profession("Husky")
        self.get_condition().immunities=["confused"]
        self.__profession_move = Skill("Growl", ["mental"], 0, 10, ["afraid"], 1, 3)
        self.__profession_dict={
            "Skill":{
                "description": "Use a special ability",
                "menu":{
                    "Growl": {
                        "name": "Growl",
                        "target": "enemies",
                        "function":self.use_growl,
                        "description": "Growls at the target, lowering their attack."
                    }
                }
            }
        }

        self.update_move_dictionary(self.__profession_dict)

    def use_growl(self,target):
        self.deliver_message(f"{self.get_name()} used Growl!\n 'GRRRRR...'\n ")
        self.perform_special_move(self, target, self.__profession_move)
        return self