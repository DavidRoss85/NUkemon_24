from src.game_objects.InfoBox import InfoBox
from src.systems.Messenger import Messenger
from src.units.Entity import Entity
import pygame

from src.units.SkillClasses import Skill

pygame.init()

def test_calculate_battle_stats():
    e=Entity("",1,100,100,2,2)
    e.calculate_start_battle_stats()

    assert e.get_battle_stats().atk==4
    assert e.get_battle_stats().blk == 1
    assert e.get_battle_stats().sk_atk == 4
    assert e.get_battle_stats().sk_blk == 1
    assert e.get_battle_stats().potency == 2
    assert e.get_battle_stats().resist == 2

def test_attack():
    e=Entity("",1,1,1,2,2)
    f=Entity("",1,1,1,2,2)
    i=InfoBox(0,0,1000,1000,"g",4)
    m=Messenger(i)
    e.calculate_start_battle_stats()
    f.calculate_start_battle_stats()
    e.set_messenger(m)
    f.set_messenger(m)

    starthp=f.get_curr_hp()
    e.attack(f)
    assert f.get_curr_hp()==starthp-3



def test_defend():
    e=Entity("",1,100,100,2,2)
    i = InfoBox(0, 0, 1000, 1000, "g", 4)
    m = Messenger(i)
    e.set_messenger(m)
    e.defend()

    assert e.get_condition().shield_up==True

def test_receive_attack():
    attack=Skill("",['physical'],10,0,["ugly"],10,1)
    e=Entity("",1,1,1,2,2)
    i=InfoBox(0,0,1000,1000,"g",4)
    m=Messenger(i)
    e.set_messenger(m)
    e.receive_attack(attack)
    assert e.get_battle_stats().effects== {"ugly":1}
    assert e.get_curr_hp() == 0


def test_calculate_defense():
    attack=Skill("",['physical'],10,0,["ugly"],10,1)
    e=Entity("",1,1,1,2,4)
    e.calculate_start_battle_stats()
    # i=InfoBox(0,0,1000,1000,"g",4)
    # m=Messenger(i)
    # e.set_messenger(m)
    assert (e.calculate_defense(["physical"]))==1.0
    assert e.calculate_defense(["heal"])==0
    # e.get_condition().affinities={"physical":100,"magic":10}
    assert e.calculate_defense(["mental"])==2.0



if __name__=="__main__":
    test_calculate_battle_stats()
    test_attack()