
#----------------------Skill-------------------------------
class Skill:
    """
    This is a class to hold skill properties
    """
    def __init__(self, name,s_type,dmg,cost,effect=None,potency=0,effect_duration=0):
        self.name = name
        self.s_type=s_type
        self.dmg=dmg
        self.cost=cost
        self.effect=effect
        self.effect_duration=effect_duration
        self.potency=potency
#-----------------------Base Stats---------------------------
class Stats:
    def __init__(self,hp,mp,strength, intel):
        self.hp = hp  #health
        self.mp = mp  # magic points
        self.strength = strength  # determines physical attributes
        self.intel=intel    #determines ability aptitude
        self.effect=dict() #status effects

#----------------------Condition-------------------------------
class Condition:
    def __init__(self):
        self.shield_up=False
        self.immunities=dict()
        self.affinities= {"physical":False}
        self.aversions={"magic":False}
        self.heal_affinity={"life":True}

