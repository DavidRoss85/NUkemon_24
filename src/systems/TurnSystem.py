from src.players.Computer import Computer

class TurnSystem:
    def __init__(self,player,enemy,messenger):
        self.__player_turn=True
        self.__battle_running=False
        self.__player=player
        self.__enemy:Computer=enemy
        self.__messenger=messenger
        self.__battle_over=False


    def set_messenger(self,messenger):
        self.__messenger=messenger

    def get_player_turn(self):
        return self.__player_turn

    def set_player_turn(self,value):
        self.__player_turn=value

    def switch_player_turn(self):
        self.__player_turn=not self.__player_turn

    def cpu_perform_action(self,perform_action):
        self.__player_turn=self.__enemy.execute_move(self.__player)

    def check_loss_conditions(self,perform_action):
        cur_char=self.__player.get_current_character()
        if cur_char.get_curr_hp()==0:
            if len(self.__player.get_team())>1:
               perform_action(
                   self.__player,
                   {
                       "name":"KO",
                       "function": self.__player.send_to_graveyard
                   },
                   {
                       "owner":self.__player,
                       "receiver": cur_char
                   }
               )
            else:
                print("GAME OVER")

    def check_win_conditions(self,perform_action):
        enemy_cur_char=self.__enemy.get_current_character()
        if enemy_cur_char.get_curr_hp()==0:
            if len(self.__enemy.get_team())>1:
                my_moves=self.__enemy.get_menu_dictionary()
                perform_action(
                    self.__enemy,
                    {
                        "name": "eKO",
                        "function": self.__enemy.send_to_graveyard
                    },
                    {
                        "owner": self.__enemy,
                        "receiver": enemy_cur_char
                    }
                )
            else:
                if not self.__battle_over:
                    perform_action(
                        self.__enemy,
                        {
                            "name": "Die",
                            "function": self.__nothing_func
                        },
                        {
                            "owner":self.__enemy,
                            "receiver": enemy_cur_char
                        }
                    )
                    self.__deliver_message(f"Congratulations!\n You have defeated the enemy!!\n "
                                           f"You earn some random amount of experience.")
                    self.__player_turn=True
                    self.__battle_over=True
                    return True

        return False

    def __deliver_message(self, message):
        self.__messenger.process_message(message)

    def __nothing_func(self,args):
        pass