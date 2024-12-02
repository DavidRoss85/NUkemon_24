from random import randint

from src.globals.UC import UC
from src.systems.Animator import Animator
from src.units.Team import Team
from src.systems.ComputerLogic import careful_AI, math_professor_ai


class Computer(Team):
    def __init__(self):
        super().__init__()
        self.__animator=None


    def set_animator(self,animator):
        self.__animator=animator

    def execute_move(self,player):
        moves=self.get_menu_dictionary()

        #<<CPU AI LOGIC GOES HERE>>
        if self.get_current_character().get_profession()=="math professor":
            return math_professor_ai(self,player,self.__animator,moves)
        else:
            return careful_AI(self,player,self.__animator,moves)


