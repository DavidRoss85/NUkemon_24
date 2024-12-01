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

    def check_loss_conditions(self,perform_action):
        cur_char=self.__player.get_current_character()
        if cur_char.get_curr_hp()==0:
            if len(self.__player.get_team())>1:
               perform_action(
                   self.__player,
                   {
                       "name":"Die",
                       "function": self.__player.send_to_graveyard
                   },
                   {
                       "owner":self.__player,
                       "receiver": cur_char
                   }
               )
            else:
                print("GAME OVER")

    def check_win_conditions(self):
        enemy_cur_char=self.__enemy.get_current_character()
        if enemy_cur_char.get_curr_hp()==0:
            if len(self.__enemy.get_team())>1:
                my_moves=self.__enemy.get_menu_dictionary()
                # print("OUCH!")
            else:
                print("YOU WIN!!")
