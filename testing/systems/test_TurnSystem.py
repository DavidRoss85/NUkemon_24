from src.game_objects.InfoBox import InfoBox
from src.systems.Messenger import Messenger
from src.systems.TurnSystem import TurnSystem
from src.units.Entity import Entity
import pygame

pygame.init()

def test_tick_status_effects():
    i=InfoBox(1,1,1,1,"")
    m=Messenger(i)
    t=TurnSystem(None,None,m,None)
    e = Entity("", 1, 100, 100, 2, 2)
    e.set_messenger(m)
    e.get_battle_stats().effects={"injured":1,"jump":2,"chip":3}

    start_health=e.get_curr_hp()

    t.tick_status_effects(e)
    assert e.get_curr_hp()<start_health

def test_decrement_status_effects():
    i=InfoBox(1,1,1,1,"")
    m=Messenger(i)
    t=TurnSystem(None,None,m,None)
    e = Entity("", 1, 100, 100, 2, 2)
    e.set_messenger(m)
    e.get_battle_stats().effects={"beat":1,"jump":2,"chip":3}

    t.decrement_status_effects(e)
    assert e.get_battle_stats().effects=={"jump":1,"chip":2}
    t.decrement_status_effects(e)
    assert e.get_battle_stats().effects == {"chip": 1}


def test_evaluate_status_effects():
    t = TurnSystem(None, None, None, None)
    e = Entity("", 1, 100, 100, 2, 2)

    e.get_battle_stats().effects = {"asleep": 1, "jump": 2, "chip": 3}
    assert t.evaluate_status_effects(e)["allowed"]==["Switch"]
    e.get_battle_stats().effects = {"injured": 1, "smarter": 2, "stronger": 3}
    assert t.evaluate_status_effects(e)["negatives"]==["injured"]
    assert t.evaluate_status_effects(e)["boost"].atk==1.2
    assert t.evaluate_status_effects(e)["boost"].sk_atk==1.2


def test_switch_player_turn():
    t = TurnSystem(None, None, None, None)
    t.set_player_turn(True)
    t.switch_player_turn()
    assert t.get_player_turn()==False

