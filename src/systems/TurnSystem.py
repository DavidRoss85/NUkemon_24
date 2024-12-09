from src.players.Computer import Computer
from src.units.SkillClasses import Skill


class TurnSystem:
    def __init__(self,player,enemy,messenger):
        self.__player_turn=True
        self.__battle_running=False
        self.__player=player
        self.__enemy:Computer=enemy
        self.__messenger=messenger
        self.__battle_over=False
        self.__player_victory=False
    # =======================================================================================================
    @staticmethod
    def evaluate_status(character,active:bool=True):
        """
        Evaluates a players effect status, counts down its timer and returns a list of moves allowed to carry out
        :param character: character being evaluated
        :param active: boolean if the user is active or not
        :return: list of allowed moves Ex: ['Switch','Attack']
        """

        allowed_moves=['all']   #Default, all moves allowed
        effects=character.get_battle_effects()
        stats=character.get_battle_stats()
        delete_list=[]
        for key,value in effects.items():
            if key=="asleep" or key=="paralyzed" or key=="frozen":
                character.deliver_message(f"{character.get_name()} is {key}.\n ")
                allowed_moves=["Switch"]
            if key=="injured":
                character.deliver_message(f"{character.get_name()} is {key}.\n ")
                character.receive_attack(
                    Skill(
                        "",
                        ["physical"],
                        stats.blk+max(stats.max_hp//20,1),
                        0
                    )
                )

            value-=1
            effects[key]=value
            if value<=0:
                delete_list.append(key)
                character.deliver_message(f"{character.get_name()} is no longer {key}.\n ")

        for effect in delete_list:
            del effects[effect]

        return allowed_moves

    def get_battle_status(self):
        if self.__battle_over and self.__player_victory:
            return "victory"
        elif self.__battle_over and not self.__player_victory:
            return "loss"
        else:
            return "ongoing"
    # =======================================================================================================
    def set_messenger(self,messenger):
        self.__messenger=messenger
    # =======================================================================================================
    def get_player_turn(self):
        return self.__player_turn
    # =======================================================================================================
    def set_player_turn(self,value):
        self.__player_turn=value
    # =======================================================================================================
    def switch_player_turn(self):
        self.__player_turn=not self.__player_turn
    # =======================================================================================================
    def cpu_perform_action(self,perform_action):
        for character in self.__enemy.get_team().values():
            if character!=self.__enemy.get_current_character():
                m= TurnSystem.evaluate_status(character,character==self.__enemy.get_current_character())

        self.__player_turn=self.__enemy.execute_move(self.__player,perform_action)

    # =======================================================================================================
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
                self.__battle_over=True
                self.__player_victory=False
    # =======================================================================================================
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
                    self.__player_victory=True
                    return True

        return False
    # =======================================================================================================
    def __deliver_message(self, message):
        self.__messenger.process_message(message)
    # =======================================================================================================
    def __nothing_func(self,args):
        return self.__enemy