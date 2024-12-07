from src.units.SkillClasses import Skill
from src.units.subcharacters.Husky import Husky
from src.units.subcharacters.LazyStudent import LazyStudent
from src.units.subcharacters.MathProfessor import MathProfessor
from src.units.subcharacters.TeachingAssistant import TeachingAssistant


class AllPowerful(Husky,LazyStudent,MathProfessor,TeachingAssistant):
    def __init__(self, name, level, hp, mp, strength, intel, sprite, x=0, y=0):
        super().__init__(name, level, hp, mp, strength, intel, sprite, x, y)
        self.set_profession("All Powerful")
        # self.__profession_move=Skill("Sleep in Class", ["heal"], 2, 10, ["asleep"], 1, 3)
        self.get_condition().immunities = []
        # self.__lazy_move_dict = {
        #     "Skill": {
        #         "menu": {
        #             "Sleep in Class": {
        #                 "name": "Sleep in Class", "target": "self", "function": self.sleep_in_class
        #             }
        #         }
        #     }
        # }

        # self.update_move_dictionary(self.__lazy_move_dict)

    def sleep_in_class(self,target):

        self.perform_special_move(self,target,self.__profession_move)
        return self