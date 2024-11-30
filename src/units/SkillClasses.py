
#----------------------Skill-------------------------------
class Skill:
    """
    This is a class to hold skill properties
    """
    def __init__(self, name,s_type,dmg,cost,effect):
        self.name = name
        self.s_type=s_type
        self.dmg=dmg
        self.cost=cost
        self.effect=effect
#-----------------------Base Stats---------------------------
class Stats:
    def __init__(self,hp,mp,strength, intel):
        self.hp = hp  #health
        self.mp = mp  # magic points
        self.strength = strength  # determines physical attributes
        self.intel=intel    #determines ability aptitude
        self.effect=[] #status effects

#----------------------Condition-------------------------------
class Condition:
    def __init__(self):
        self.shield_up=False
        self.affinities= {"physical":False}
        self.aversions={"magic":False}
        self.heal_affinity={"life":True}

