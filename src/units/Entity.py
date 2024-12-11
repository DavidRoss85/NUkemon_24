import copy
from random import randint

from src.globals.balance import  VARIABILITY, SHIELD_MULTIPLIER
from src.systems.TurnSystem import TurnSystem
from src.units.SkillClasses import *
from src.utils.utils import merge_dictionaries

class Entity:
    """
    Base class that forms the basis for all characters in the game.
    Entities represent a unit's basic stats and abilities
    """
    def __init__(self,name,level,hp,mp,strength,intel):
        self.__name=name    #Name
        self.__level = level    #Level
        self.__base_stats=Stats(hp,mp,strength,intel)   #Base stats. These are not affected in battle
        self.__battle_stats=Stats(hp,mp,strength,intel) #Battle stats. These change in battle but return to normal when it ends
        self.__condition=Condition()    #Unit condition such as effects and status
        self.__owner=self   #Owner of this character (ie Player or Computer)
        self.__profession=None  #Used by child classes
        self.__messenger=None   #Handles messages

        #Basic attack skill:
        self.__attack_move=Skill(
            "Punch",
            ["physical"],
            self.__base_stats.strength,
            0,
            None
        )

        #List of moves. Child classes can add to these to create longer moves lists
        self.__move_dict={
            "Attack": {
                "name": "Attack",
                "target": "active",
                "function":self.attack,
                "description": "Attack the target"
            },
            "Defend":{
                "name": "Defend",
                "target":"self",
                "function":self.defend,
                "description": "Defend against the next move"
            },
        }

    #=======================================================================================================
    #Getters:
    def get_name(self):
        return self.__name

    def get_max_hp(self):
        return self.__battle_stats.max_hp

    def get_curr_hp(self):
        return self.__battle_stats.hp

    def get_max_mp(self):
        return self.__battle_stats.max_mp

    def get_curr_mp(self):
        return self.__battle_stats.mp

    def get_base_strength(self):
        return self.__base_stats.strength

    def get_battle_strength(self):
        return self.__battle_stats.strength

    def get_battle_stats(self):
        return self.__battle_stats

    def get_base_intel(self):
        return self.__base_stats.intel

    def get_battle_intel(self):
        return self.__battle_stats.intel

    def get_level(self):
        return self.__level

    def get_move_list(self)->list:
        return list(self.__move_dict.keys())

    def get_move_dictionary(self):
        return self.__move_dict

    def get_battle_effects(self):
        return self.__battle_stats.effects

    def get_owner(self):
        return self.__owner

    def get_profession(self):
        return self.__profession

    def get_condition(self):
        return self.__condition
    #=======================================================================================================
    #Setters
    def set_name(self,name):
        self.__name=name

    def set_max_hp(self,hp):
        self.__base_stats.hp=hp
    def set_curr_hp(self,hp):
        #Set HP:
        self.__battle_stats.hp=hp
        #Health shouldn't dip below 0:
        if self.__battle_stats.hp<0:
            self.__battle_stats.hp=0
        #Ensure health doesn't go above max
        if self.__battle_stats.hp>self.__battle_stats.max_hp:
            self.__battle_stats.hp=self.__battle_stats.max_hp

    def set_max_mp(self,mp):
        self.__base_stats.mp=mp

    def set_curr_mp(self,mp):
        self.__battle_stats.mp=mp
        # MP shouldn't dip below 0:
        if self.__battle_stats.mp < 0:
            self.__battle_stats.mp = 0
        #Ensure doesn't go above max
        if self.__battle_stats.mp>self.__battle_stats.max_mp:
            self.__battle_stats.mp=self.__battle_stats.max_mp

    def set_base_strength(self,strength):
        self.__base_stats.strength=strength

    def set_battle_strength(self,strength):
        self.__battle_stats.strength=strength

    def set_base_intel(self,intel):
        self.__base_stats.intel=intel

    def set_battle_intel(self,intel):
        self.__battle_stats.intel=intel

    def set_level(self,level):
        self.__level=level

    def set_owner(self,owner):
        self.__owner=owner

    def set_profession(self,profession):
        self.__profession=profession

    def set_messenger(self,messenger):
        self.__messenger=messenger

    def set_condition(self,condition:Condition):
        self.__condition=condition
    #=======================================================================================================
    def calculate_start_battle_stats(self):
        """
        Battle stats are calculated from base stats. At the start of battle.
        Battle stats are normal, but effects can modify them
        Battle stats return to normal after battle ends.
        """
        #Copy base stats to battle stats
        self.__battle_stats=copy.deepcopy(self.__base_stats)
        #Update the battle stats using calculations
        self.get_battle_stats().update_calculations(self.__level)

    #=======================================================================================================

    def perform_special_move(self,user,target,move):
        """
        Child classes call on this to perform special moves. This handles all
        the calculations before delivering the move
        :param user: Unit executing the move
        :param target: Receives the move
        :param move: The action being performed
        """
        self.execute_move()
        #Get battle stats
        stats = copy.deepcopy(user.get_battle_stats())

        #Modify battle stats from temporary statuses:
        user_effects=TurnSystem.evaluate_status_effects(user)
        boosts=user_effects["boost"]

        #For each boost, multiply it by the stats
        for key in vars(boosts):
            if key=="effects":continue  #This is not multiplyable
            factor=getattr(boosts,key)
            base=getattr(stats,key)
            setattr(stats,key,base*factor)


        current_move = copy.deepcopy(move)
        determiner=stats.sk_atk
        #If the skill is a physical attack the damage effect will depend on user's attack vs skill power
        if "physical" in current_move.s_types:
            determiner=stats.atk

        #Calculate skill power or potency of effect:
        #Add between 0-10 percent of ATK/SKL_ATK/Potency to itself to determine dmg or effect
        if user.get_curr_mp()>= current_move.cost:
            user.set_curr_mp(user.get_curr_mp() - current_move.cost)
            current_move.dmg = (determiner + randint(0, int(determiner * VARIABILITY))) * current_move.dmg
            current_move.potency += (stats.potency + randint(0, int(stats.potency * VARIABILITY))) * current_move.potency
            target.receive_attack(current_move)
        else:
            #user did not have enough mp (Will lose a turn)
            user.deliver_message(f"Not enough mp.\n ")
    # =======================================================================================================
    def execute_move(self):
        """
        Call this function whenever the user tries to execute a move
        """
        # Drop shields to execute a move
        self.__condition.shield_up = False
    #=======================================================================================================
    def attack(self,target=None):
        """
        Carry out a physical attack. Calls the target's receive_attack method.
        :param target: Receiver of the attack
        """
        #Get ready to execute a move
        self.execute_move()

        #Ensure there is a target
        if target is None:
            target=self

        #Confusion causes a player to attack themselves
        if "confused" in self.__battle_stats.effects:
            self.deliver_message(f"{self.__name} is confused and attacks themself...\n ")
            target=self

        #MATH TO CALCULATE ATTACK: (BASE STR * MULTIPLIER + VARIABILITY)
        current_move= copy.deepcopy(self.__attack_move)
        base_damage=self.__battle_stats.atk
        current_move.dmg= base_damage + randint(0,int(base_damage*VARIABILITY))

        #Deliver message and attack to target
        self.deliver_message(f"{self.__name} attacks with {self.__attack_move.name}!\n ")
        target.receive_attack(current_move)

        #Return the target owner
        return target.get_owner()
    #=======================================================================================================
    def defend(self,args=None):
        """
        Double defense but lose a turn
        :param args: Arguments
        """
        self.deliver_message(f"{self.__name} guards themself.\n ")
        self.__condition.shield_up=True
        return self.get_owner()

    #=======================================================================================================
    def receive_attack(self,attack):
        """
        Any attack/heal/skill carried out is received here by the target.
        Depending on what is contained in the attack object will determine the outcome
        """

        final_dmg=attack.dmg    #Final damage starts at attack damage

        #Total damage is reduced by defense: (Depends on str or intel based on attack type)
        defense= self.calculate_defense(attack.s_types)
        final_dmg = max(final_dmg-defense,0)

        #Check for affinities and aversions:
        final_dmg=self.calculate_affinity(final_dmg,attack)

        #Calculate heals if applicable:
        res=self.calculate_heals(final_dmg,attack)
        if res["heal"]:
            # Update message
            self.deliver_message(f"{self.__name} is healed for {res["damage"]} points of health.\n ")
            final_dmg=res["damage"]*-1
        else:
            # Update message
            if res["damage"]>0:
                self.deliver_message(f"{self.__name} receives {res["damage"]} points of damage.\n ")

            final_dmg=res["damage"]


        #Status effects. More intel resists status effects based on their potency:
        self.calculate_status_effect(attack)
        self.set_curr_hp(self.get_curr_hp()-final_dmg)


    #=======================================================================================================
    def update_move_dictionary(self, move):
        self.__move_dict.update(merge_dictionaries(move,self.__move_dict))
    #=======================================================================================================
    def stub_command(self):
        pass
    #=======================================================================================================
    def deliver_message(self, message):
        self.__messenger.process_message(message)
        print(f"Entity:{message}")
    #=======================================================================================================

    def calculate_defense(self,s_types):
        # Roll dice to determine defense against attack:
        if "heal" in s_types or "life" in s_types:
            return 0
        defense=0
        if "physical" in s_types:
            defense = self.__battle_stats.blk
            defense = defense + randint(0, int(defense * VARIABILITY))
        elif "mental" in s_types:
            defense = self.__battle_stats.sk_blk
            defense = defense + randint(0, int(defense * VARIABILITY))

        # Shield doubles defense:
        if self.__condition.shield_up:
            defense *= SHIELD_MULTIPLIER
        return defense
    #=======================================================================================================
    def calculate_affinity(self,final_dmg,attack):
        """
        Determines the affinity effect of an attack
        Affinities lower the damage or double the positive effects of some moves
        Aversion increase the damage or reduce the positive effects of some moves
        :param final_dmg: Starting damage
        :param attack: Attack object
        :return: Modified damage
        """
        #Get affinities player affinities and aversions
        affinities = self.__condition.affinities
        aversions = self.__condition.aversions

        #Check for the attack type: Ex "physical", "mental", "fire", "ice"
        for s_type in attack.s_types:
            if s_type in affinities:
                # Update message
                self.deliver_message(f"{self.__name} is resistant to {attack.name}.\n")
                # Get multiplier factor:
                reduction_factor = affinities[attack.s_types]
                final_dmg = int(final_dmg * reduction_factor)

            # Check for aversions:
            if s_type in aversions:
                # Update message
                self.deliver_message(f"{attack.name} is very effective!\n")
                # Get multiplier factor:
                increase_factor = aversions[attack.s_types]
                final_dmg = int(final_dmg * increase_factor)

        return final_dmg
    # =======================================================================================================
    def calculate_heals(self,final_dmg,attack):
        """
        Heal types increase health
        :param final_dmg: Starting "damage/heal"
        :param attack: Skill object
        """
        heals = self.__condition.heal_affinity
        # Check for healing:
        is_heal = False  # Check if "Attack heals"
        if "heal" in attack.s_types and "heal" in heals:
            # Get multiplier factor:
            increase_factor = heals["heal"]
            final_dmg = int(final_dmg * increase_factor)
            # Healers give health:
            is_heal = True
        if "life" in attack.s_types and "life" in heals:
            increase_factor = heals["life"]
            final_dmg = int(final_dmg * increase_factor)
            # Healers give health:
            is_heal = True

        return {"heal":is_heal,"damage":int(final_dmg)}
    # =======================================================================================================
    def calculate_status_effect(self,attack):
        """
        Applies, modifies or removes status effects based on the attack.
        Attack types "remedy" fix anything in their list beginning with "un-".
        For example: {s_type:"remedy", effect: "un-confused"} fixes "confused" status
        :param attack: Skill object containing details of the attack
        """
        remedy=False
        #Attack has effects:
        if attack.effects is not None:
            #Check if status is a remedy
            if "remedy" in attack.s_types:remedy=True

            #Check each status effect:
            for effect in attack.effects:
                #Check for remedies to statuses and fix:
                if remedy:
                    if effect[0:3]=="un-":
                        effect=effect[3:]
                        if effect in self.__battle_stats.effects:
                            del self.__battle_stats.effects[effect]
                            self.deliver_message(f"{self.get_name()} is no longer {effect}.\n ")
                            continue
                # Check for immunity:
                if effect in self.__condition.immunities:
                    self.deliver_message(f"{self.get_name()} is immune to being {effect}.\n ")
                    continue

                #Not immune:
                #Calculate resistance:
                resistance=self.__battle_stats.resist
                resistance+=randint(0,int(resistance*VARIABILITY))

                #If not resistant enough
                if attack.potency>resistance:
                    #implement effect if not already under the effect
                    if effect not in self.__battle_stats.effects:
                        self.deliver_message(f"{self.get_name()} is {effect}.\n ")
                        self.__battle_stats.effects[effect]=attack.effect_duration
                    else:
                        self.deliver_message(f"{self.get_name()} is already {effect}.\n ")

