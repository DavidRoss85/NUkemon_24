import copy
import random
from random import randint

from src.globals.balance import ATK_MULTIPLIER, VARIABILITY, DEF_MULTIPLIER, SHIELD_MULTIPLIER, SKL_DEF_MULTIPLIER, \
    SKL_RESIST_MULTIPLIER
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
        self.__attack_move=Skill("Punch",["physical"],self.__base_stats.strength,0,None)
        self.__move_dict={
            "Attack": {"name": "Attack", "target": "active", "function":self.attack},
            "Defend":{"name": "Defend", "target":"self","function":self.defend},
        }

    #=======================================================================================================
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

    #=======================================================================================================
    def attack(self,target=None):

        if target is None:
            target=self

        if "confused" in self.__battle_stats.effects:
            self.deliver_message(f"{self.__name} is confused and attacks themself...\n ")
            target=self

        #MATH TO CALCULATE ATTACK: (BASE STR * MULTIPLIER + VARIABILITY)
        current_move= copy.deepcopy(self.__attack_move)
        base_damage=self.__battle_stats.strength * ATK_MULTIPLIER
        current_move.dmg= base_damage + randint(0,int(base_damage*VARIABILITY))

        self.deliver_message(f"{self.__name} attacks with {self.__attack_move.name}!\n ")
        target.receive_attack(current_move)
        return target.get_owner()
    #=======================================================================================================
    def defend(self,args=None):
        self.deliver_message(f"{self.__name} guards themself.\n ")
        self.__condition.shield_up=True
        return self.get_owner()

    #=======================================================================================================
    def receive_attack(self,attack):

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
            self.deliver_message(f"{self.__name} receives {res["damage"]} points of damage.\n ")
            final_dmg=res["damage"]


        #Status effects. More intel resists status effects based on their potency:
        self.calculate_status_effect(attack)
        self.set_curr_hp(self.get_curr_hp()-final_dmg)

    #=======================================================================================================
    def execute_move(self,command):
        self.__condition.shield_up=False
        # self.__move_dict[command]()
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
            defense = self.__battle_stats.strength * DEF_MULTIPLIER
            defense = defense + randint(0, int(defense * VARIABILITY))
        elif "mental" in s_types:
            defense = self.__battle_stats.intel * SKL_DEF_MULTIPLIER
            defense = defense + randint(0, int(defense * VARIABILITY))

        # Shield doubles defense:
        if self.__condition.shield_up:
            defense *= SHIELD_MULTIPLIER
        return defense
    #=======================================================================================================
    def calculate_affinity(self,final_dmg,attack):
        affinities = self.__condition.affinities
        aversions = self.__condition.aversions


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
        if attack.effects is not None:
            #Check for immunity:
            for effect in attack.effects:
                if effect in self.__condition.immunities:
                    self.deliver_message(f"{self.get_name()} is immune.\n ")
                    continue
                #Calculate resistance:
                resistance=self.__battle_stats.intel*SKL_RESIST_MULTIPLIER
                resistance+=randint(0,int(resistance*VARIABILITY))
                if attack.potency>resistance:
                    if effect not in self.__battle_stats.effects:
                        self.deliver_message(f"{self.get_name()} is {effect}.\n ")
                        self.__battle_stats.effects[effect]=attack.effect_duration
                    else:
                        self.deliver_message(f"{self.get_name()} is already {attack.effects}.\n ")