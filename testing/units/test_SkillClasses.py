from src.units.SkillClasses import *

def test_update_calculations():
    stats=Stats(1,1,1,1)
    stats.update_calculations(1)
    assert stats.atk==4
    assert stats.blk == 1
    assert stats.sk_atk == 4
    assert stats.sk_blk == 1
    assert stats.potency == 2
    assert stats.resist == 2

if __name__=="__main__":
    test_update_calculations()
