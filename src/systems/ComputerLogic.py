from random import randint



def careful_AI(player,computer,animator,move_dictionary):

    me=computer.get_current_character()
    health_percent=(me.get_curr_hp()/me.get_max_hp())*100

    num=randint(1,10)

    if num>1 and health_percent > 50:
        move_dictionary["Attack"]["function"](player.get_current_character())
        animator.pause_and_animate({"subject":computer,"action":"Attack"})
        animator.pause_and_animate({"object": player, "action": "Attack"})
    else:
        move_dictionary["Defend"]["function"](computer.get_current_character())

    return True

def berserk_AI(player,computer,animator,move_dictionary):
    move_dictionary["Attack"]["function"](player.get_current_character())
    animator.pause_and_animate({"subject": computer, "action": "Attack"})
    animator.pause_and_animate({"object": player, "action": "Attack"})

    return True