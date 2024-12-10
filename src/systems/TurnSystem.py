from src.players.Computer import Computer
from src.units.SkillClasses import Skill


class TurnSystem:
    """
    Handles the turns in the game as well as win/lose conditions
    """
    def __init__(self,player,enemy,messenger,animator):
        self.__player_turn=True
        self.__battle_running=False
        self.__player=player
        self.__enemy:Computer=enemy
        self.__messenger=messenger
        self.__animator=animator
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

        #Get effects and status:
        effects=character.get_battle_effects()
        stats=character.get_battle_stats()

        #Keeps a list of statuses/effects to remove
        delete_list=[]

        #key is name of effect, value is how many turns left
        for key,value in effects.items():
            #Player is immobile:
            if key=="asleep" or key=="paralyzed" or key=="frozen":
                character.deliver_message(f"{character.get_name()} is {key}.\n ")
                allowed_moves=["Switch"]

            #Player will lose health each turn if injured
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

            #Decrement the value:
            value-=1
            effects[key]=value

            #If effect has run out, remove it from list:
            if value<=0:
                delete_list.append(key)
                character.deliver_message(f"{character.get_name()} is no longer {key}.\n ")

        #Delete all effects scheduled for deletion:
        for effect in delete_list:
            del effects[effect]

        #Return a list of moves allowed
        return allowed_moves
    # =======================================================================================================
    def get_battle_status(self):
        """
        :return: "victory", "loss", "ongoing"
        """
        if self.__battle_over and self.__player_victory:
            return "victory"
        elif self.__battle_over and not self.__player_victory:
            return "loss"
        else:
            return "ongoing"
    # =======================================================================================================
    def set_messenger(self,messenger):
        """
        Set messenger
        :param messenger: Messenger
        """
        self.__messenger=messenger
    # =======================================================================================================
    def get_player_turn(self):
        """
        :return: True/False
        """
        return self.__player_turn
    # =======================================================================================================
    def set_player_turn(self,value):
        """
        Set player turn
        :param value: True/False
        """
        self.__player_turn=value
    # =======================================================================================================
    def switch_player_turn(self):
        """
        Switch player turn from False to True or True to False
        """
        self.__player_turn=not self.__player_turn

    # =======================================================================================================
    def perform_action(self, subject, verb, o_ject):
        """
        Handles actions performed by player and enemy and schedules animations
        :param subject: Actor performing the action
        :param verb: Dictionary with the action to be performed
        :param o_ject: Dictionary containing the receiver of action and owner
        """
        o_ject["owner"].freeze_frame()

        # Evaluate the current character status and only do move if allowed:
        allowed_moves = TurnSystem.evaluate_status(subject.get_current_character())
        if (len(allowed_moves) == 0 or verb["name"] not in allowed_moves) and "all" not in allowed_moves:
            o_ject["owner"].unfreeze_frame()
            return

        # Execute the stored function on the target (current_character)
        owner = verb["function"](o_ject["receiver"])

        # Add an animation to the paused animation __queue
        # Game events will wait for these animations to complete
        self.__animator.pause_and_animate({
            "subject": subject,
            "action": verb["name"]
        })

        self.__animator.pause_and_animate({
            "object": owner,
            "action": verb["name"]
        })

    # =======================================================================================================
    def cpu_perform_action(self):
        """
        Evaluate computer status and perform actions
        """
        #Check teammates statuses:
        for character in self.__enemy.get_team().values():
            if character!=self.__enemy.get_current_character():
                m= TurnSystem.evaluate_status(character,character==self.__enemy.get_current_character())

        #Execute move by computer (Current character status is evaluated in perform move
        self.__player_turn=self.__enemy.execute_move(self.__player,self.perform_action)

    # =======================================================================================================
    def check_loss_conditions(self):
        """
        Controls KO of player and Game Over
        """
        #Get player current character
        cur_char=self.__player.get_current_character()
        ko={"name":"KO", "function": self.__player.send_to_graveyard}
        myself={"owner":self.__player,"receiver": cur_char}

        #Check current character HP
        if cur_char.get_curr_hp()==0:

            #If it dips below 0, switch to next character if available
            if len(self.__player.get_team())>1:
               self.perform_action(self.__player,ko,myself)

            #Otherwise Game Over
            else:
                print("GAME OVER")
                self.__battle_over=True
                self.__player_victory=False

    # =======================================================================================================
    def check_win_conditions(self):
        """
        Controls KO of computer and Victory
        """
        #Get enemy current character
        enemy_cur_char=self.__enemy.get_current_character()
        ko={"name": "eKO", "function": self.__enemy.send_to_graveyard}
        die={"name": "Die", "function": self.__nothing_func}
        myself={"owner": self.__enemy,"receiver": enemy_cur_char}


        #Check Enemy HP
        if enemy_cur_char.get_curr_hp()==0: #If HP below 0

            #Switch to next character if available
            if len(self.__enemy.get_team())>1:

                # my_moves=self.__enemy.get_menu_dictionary()
                #Enemy KO
                self.perform_action(self.__enemy,ko,myself)
            else:
                #Do victory routine:
                if not self.__battle_over:
                    self.perform_action(self.__enemy,die,myself)

                    self.__deliver_message(f"Congratulations!\n You have defeated the enemy!!\n "
                                           f"You earn some random amount of experience.")
                    self.__player_turn=True
                    self.__battle_over=True
                    self.__player_victory=True
                    return True

        return False
    # =======================================================================================================
    def __deliver_message(self, message):
        """
        Deliver messages
        :param message: String to send to messenger
        """
        self.__messenger.process_message(message)
    # =======================================================================================================
    def __nothing_func(self,args):
        """Nothing"""
        return self.__enemy