
from src.units.Team import Team
from src.systems.ComputerLogic import ai_dictionary #contains a list of the functions that govern cpu behavior


class Computer(Team):
    """
    This is the computer object that controls computer actions. Inherits from Team
    """
    def __init__(self):
        super().__init__()
        self.__animator=None


    def set_animator(self,animator):
        self.__animator=animator

    def execute_move(self,player,action_function):

        #retrieve the moves dictionary for the computer:
        moves=self.get_menu_dictionary()

        res=0   #initialize

        #Get current profession and choose AI based on that:
        profession=self.get_current_character().get_profession()
        if profession in ai_dictionary:
            res= ai_dictionary[profession](self,player,moves,action_function)
        else:
            res= ai_dictionary["generic"](self,player,moves,action_function)

        return res
