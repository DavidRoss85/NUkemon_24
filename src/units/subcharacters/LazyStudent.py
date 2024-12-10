
from src.units.SkillClasses import Skill
from src.units.Character import Character


class LazyStudent(Character):
    """Student with lazy characteristics"""
    def __init__(self, name, level, hp, mp, strength, intel, sprite, x=0, y=0):
        super().__init__(name, level, hp, mp, strength, intel, sprite, x, y)
        self.set_profession("Lazy Student")
        self.__profession_move=Skill("Sleep in Class", ["heal"], 2.5, 10, ["asleep"], 1, 4)
        self.get_condition().immunities = []
        self.__profession_dict = {
            "Skill": {
                "description": "Use a special ability",
                "menu": {
                    "Sleep in Class": {
                        "name": "Sleep in Class",
                        "target": "self",
                        "function": self.sleep_in_class,
                        "description": "Student falls asleep for 3 turns, but recovers health in the process."
                    }
                }
            }
        }

        self.update_move_dictionary(self.__profession_dict)

    def sleep_in_class(self,target):
        self.deliver_message(f"{self.get_name()} falls asleep 'Zzz'...\n ")
        self.perform_special_move(self,target,self.__profession_move)
        return self