import random
from random import randint

from src.systems.Messenger import Messenger
from src.units.SkillClasses import *
from src.utils.utils import merge_dictionaries

#Declare constants for game tuning
ATTACK_DICE = 6
DEFEND_DICE = 2
DEFENSE_MULTIPLIER = 2
AVERSION_MULTIPLIER=2
AFFINITY_REDUCTION=2
def roll_die(sides):
    return random.randint(1,sides)


class Entity:
    def __init__(self,name,level,hp,mp,strength,intel):
        self.__name=name
        self.__level = level
        self.__base_stats=Stats(hp,mp,strength,intel)
        self.__battle_stats=Stats(hp,mp,strength,intel)
        self.__condition=Condition()
        self.__target=self
        self.__owner=self
        self.__profession=None
        self.__messenger=None
        self.__attack_move=Skill("Punch","physical",self.__base_stats.strength,0,None)
        self.__move_dict={
            "Attack": {"name": "Attack", "target": "active", "function":self.attack},
            "Defend":{"name": "Defend", "target":"self","function":self.defend},
        }


    #Getters:
    def get_name(self):
        return self.__name

    def get_max_hp(self):
        return self.__base_stats.hp

    def get_curr_hp(self):
        return self.__battle_stats.hp

    def get_max_mp(self):
        return self.__base_stats.mp

    def get_curr_mp(self):
        return self.__battle_stats.mp

    def get_base_strength(self):
        return self.__base_stats.strength

    def get_battle_strength(self):
        return self.__battle_stats.strength

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

    def get_target(self):
        return self.__target

    def get_battle_effects(self):
        return self.__battle_stats.effects

    def get_owner(self):
        return self.__owner

    def get_profession(self):
        return self.__profession

    def get_condition(self):
        return self.__condition

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
        if self.__battle_stats.hp>self.__base_stats.hp:
            self.__battle_stats.hp=self.__base_stats.hp

    def set_max_mp(self,mp):
        self.__base_stats.mp=mp

    def set_curr_mp(self,mp):
        self.__battle_stats.mp=mp

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

    def set_target(self,target):
        self.__target=target

    def set_messenger(self,messenger):
        self.__messenger=messenger


    def set_condition(self,condition:Condition):
        self.__condition=condition


    def attack(self,target=None):

        if target is None:
            target=self

        if "confused" in self.__battle_stats.effects:
            self.deliver_message(f"{self.__name} is confused...\n ")
            target=self

        #MATH TO CALCULATE ATTACK:
        self.__attack_move.dmg= self.__battle_stats.strength * roll_die(ATTACK_DICE)

        self.deliver_message(f"{self.__name} attacks with {self.__attack_move.name} for {self.__attack_move.dmg}!\n ")
        target.receive_attack(self.__attack_move)
        return target.get_owner()

    def defend(self,args=None):
        self.deliver_message(f"{self.__name} guards themself.\n ")
        self.__condition.shield_up=True
        return self.get_owner()

    def receive_attack(self,attack):
        is_heal=False   #Check if "Attack heals"
        final_dmg=attack.dmg    #Final damage starts at attack damage

        #Roll dice to determine defense against attack:
        defense=self.__battle_stats.strength * roll_die(DEFEND_DICE)
        #Shield doubles defense:
        if self.__condition.shield_up:
            defense*=DEFENSE_MULTIPLIER
        #Total damage is reduced by defense:
        final_dmg = max(final_dmg-defense,0)

        #Check for affinities:
        if (self.__condition.affinities.get(attack.s_type) is not None and
            self.__condition.affinities.get(attack.s_type) is True):

            #Update message
            self.deliver_message(f"{self.__name} is resistant to {attack.name} attack.\n")
            #Affinities only deliver half damage
            final_dmg=int(final_dmg/AFFINITY_REDUCTION)

        # Check for aversions:
        if (self.__condition.aversions.get(attack.s_type) is not None and
                self.__condition.affinities.get(attack.s_type) is True):
            # Update message
            self.deliver_message(f"{attack.name} is very effective!\n")
            # Aversions do double damage:
            final_dmg = int(final_dmg *AVERSION_MULTIPLIER)

        #Check for healing:
        if (self.__condition.heal_affinity.get(attack.s_type) is not None and
                self.__condition.affinities.get(attack.s_type) is True):
            # Update message
            self.deliver_message(f"HP UP\n")
            # Healers give health:
            is_heal=True

        if is_heal:
            # Update message
            self.deliver_message(f"{self.__name} is healed for {final_dmg} points of health.\n ")
            # Add to health:
            self.set_curr_hp(self.__battle_stats.hp+final_dmg)
        else:
            #Update message
            self.deliver_message(f"{self.__name} receives {final_dmg} points of damage.\n ")
            #Subtract final damage from health:
            self.set_curr_hp(self.__battle_stats.hp-final_dmg)

        #Status effects. More intel resists status effects based on their potency:
        if attack.effects is not None:
            #Check for immunity:
            if attack.effects in self.__condition.immunities:
                self.deliver_message(f"{self.get_name()} is immune to {attack.effects}.\n ")
                return

            #Calculate resistance:
            resistance=self.__battle_stats.intel+randint(0,6)
            if attack.potency>resistance:
                if attack.effects not in self.__battle_stats.effects:
                    self.deliver_message(f"{self.get_name()} is {attack.effects}.\n ")
                    self.__battle_stats.effects[attack.effects]=attack.effect_duration


    def execute_move(self,command):
        self.__condition.shield_up=False
        # self.__move_dict[command]()

    def update_move_dictionary(self, move):
        self.__move_dict.update(merge_dictionaries(move,self.__move_dict))

    def stub_command(self):
        pass

    def deliver_message(self, message):
        self.__messenger.process_message(message)
        print(f"Entity:{message}")
