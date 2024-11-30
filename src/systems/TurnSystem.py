from src.players.Computer import Computer

class TurnSystem:
    def __init__(self,player,enemy):
        self.__player_turn=True
        self.__battle_running=False
        self.__player=player
        self.__enemy:Computer=enemy


    def get_player_turn(self):
        return self.__player_turn

    def set_player_turn(self,value):
        self.__player_turn=value

    def switch_player_turn(self):
        self.__player_turn=not self.__player_turn

    def cpu_perform_action(self):
        self.__player_turn=self.__enemy.execute_move(self.__player)