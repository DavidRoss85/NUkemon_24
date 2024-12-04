from src.globals.balance import ATK_MULTIPLIER, DEF_MULTIPLIER, SKL_ATK_MULTIPLIER, SKL_DEF_MULTIPLIER, SKL_MULTIPLIER, \
    SKL_RESIST_MULTIPLIER, HP_MULTIPLIER, MP_MULTIPLIER


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
        self.max_hp=hp
        self.max_mp=mp
        self.hp = hp  #health
        self.mp = mp  # magic points
        self.strength = strength  # determines physical attributes
        self.intel=intel    #determines ability aptitude
        self.atk=0
        self.blk=0
        self.sk_atk=0
        self.sk_blk=0
        self.potency=0
        self.resist=0
        self.effects=dict() #status effects

    def update_calculations(self,level=1):
        self.max_hp=self.strength*HP_MULTIPLIER*level
        self.max_mp=self.intel*MP_MULTIPLIER*level
        self.hp=self.max_hp
        self.mp=self.max_mp
        self.atk=self.strength*ATK_MULTIPLIER*level
        self.blk=self.strength*DEF_MULTIPLIER*level
        self.sk_atk=self.intel*SKL_ATK_MULTIPLIER*level
        self.sk_blk=self.intel*SKL_DEF_MULTIPLIER*level
        self.potency=self.intel*SKL_MULTIPLIER*level
        self.resist=self.intel*SKL_RESIST_MULTIPLIER*level

#----------------------Condition-------------------------------
class Condition:
    def __init__(self):
        self.shield_up=False
        self.immunities=[]
        self.affinities= {} #physical: .5
        self.aversions={} #magic: 2
        self.heal_affinity={"heal":1,"life":1} #life:1

