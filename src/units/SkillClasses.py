
#----------------------Skill-------------------------------
class Skill:
    """
    This is a class to hold skill properties
    """
    def __init__(self, name,s_types,dmg,cost,effects=None,potency=0,effect_duration=0):
        self.name = name
        self.s_types=s_types
        self.dmg=dmg
        self.cost=cost
        self.effects=effects
        self.effect_duration=effect_duration
        self.potency=potency
#-----------------------Base Stats---------------------------
class Stats:
    def __init__(self,hp,mp,strength, intel):
        self.hp = hp  #health
        self.mp = mp  # magic points
        self.strength = strength  # determines physical attributes
        self.intel=intel    #determines ability aptitude
        self.effects=dict() #status effects

#----------------------Condition-------------------------------
class Condition:
    def __init__(self):
        self.shield_up=False
        self.immunities=[]
        self.affinities= {} #physical: .5
        self.aversions={} #magic: 2
        self.heal_affinity={"heal":1,"life":1} #life:1

