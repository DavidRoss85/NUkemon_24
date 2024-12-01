from random import randint



def careful_AI(computer,player,animator,move_dictionary):

    me=computer.get_current_character()
    health_percent=(me.get_curr_hp()/me.get_max_hp())*100

    num=randint(1,10)

    if num>1 and health_percent > 30:
        move_dictionary["Attack"]["function"](player.get_current_character())
        animator.pause_and_animate({"subject":computer,"action":"Attack"})
        animator.pause_and_animate({"object": player, "action": "Attack"})
    else:
        decision=randint(1,10)
        if len(computer.get_team())>1 and decision>=5:
            for name in computer.get_team():
                if name!=computer.get_current_character().get_name():
                    computer.freeze_frame()
                    move_dictionary["Switch"]["function"](computer.get_team()[name])
                    animator.pause_and_animate({"subject": computer, "action": "eSwitch"})
                    animator.pause_and_animate({"object": computer, "action": "eSwitch"})
                    break
        elif randint(1, 10)>5:
            move_dictionary["Defend"]["function"](computer.get_current_character())
            animator.pause_and_animate({"subject": computer, "action": "Defend"})
            animator.pause_and_animate({"object": computer, "action": "Defend"})
        else:
            move_dictionary["Attack"]["function"](player.get_current_character())
            animator.pause_and_animate({"subject": computer, "action": "Attack"})
            animator.pause_and_animate({"object": player, "action": "Attack"})

    return True

def berserk_AI(computer,player,animator,move_dictionary):
    move_dictionary["Attack"]["function"](player.get_current_character())
    animator.pause_and_animate({"subject": computer, "action": "Attack"})
    animator.pause_and_animate({"object": player, "action": "Attack"})

    return True