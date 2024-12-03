from random import randint

from src.globals.UC import UC
from src.systems.Animator import Animator
from src.units.Team import Team
from src.systems.ComputerLogic import ai_dictionary #contains a list of the functions that govern cpu behavior


class Computer(Team):
    def __init__(self):
        super().__init__()
        self.__animator=None


    def set_animator(self,animator):
        self.__animator=animator

    def execute_move(self,player):
        moves=self.get_menu_dictionary()

        #<<CPU AI LOGIC GOES HERE>>
        profession=self.get_current_character().get_profession()
        if profession in ai_dictionary:
            return ai_dictionary[profession](self,player,self.__animator,moves)
        else:
            return ai_dictionary["generic"](self,player,self.__animator,moves)


