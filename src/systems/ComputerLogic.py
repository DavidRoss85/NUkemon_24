from random import randint


def careful_ai(computer,player,move_dictionary,action=None):

    #Moves List:
    attack=move_dictionary["Attack"]
    switch=move_dictionary["Switch"]
    switch["name"]="eSwitch"
    defend=move_dictionary["Defend"]

    my_character=computer.get_current_character()
    target=player.get_current_character()
    target_owner=player

    o_ject={"owner": target_owner, "receiver": target}
    myself={"owner": computer, "receiver":my_character}
    health_percent=(my_character.get_curr_hp()/my_character.get_max_hp())*100

    num=randint(1,10)

    if num>1 and health_percent > 30:
        action(computer, attack, o_ject)
    else:
        decision=randint(1,10)
        if len(computer.get_team())>1 and decision>=5:
            for name in computer.get_team():
                if name!=computer.get_current_character().get_name():
                    computer.freeze_frame()
                    myself["receiver"] = computer.get_team()[name]
                    action(computer, switch, myself)
                    break
        elif randint(1, 10)>5:
           action(computer, defend, myself)
        else:
            action(computer, attack, o_ject)

    return True

def berserk_ai(computer,player,move_dictionary,action=None):


    #Moves List:
    attack=move_dictionary["Attack"]
    switch=move_dictionary["Switch"]
    switch["name"]="eSwitch"
    defend=move_dictionary["Defend"]

    my_character=computer.get_current_character()
    target=player.get_current_character()
    target_owner=player

    o_ject={"owner": target_owner, "receiver": target}
    myself={"owner": computer, "receiver":my_character}
    health_percent=(my_character.get_curr_hp()/my_character.get_max_hp())*100

    num=randint(1,10)
    action(computer,attack,o_ject)
    return True


def math_professor_ai(computer,player,move_dictionary,action=None):

    #Moves List:
    attack=move_dictionary["Attack"]
    discreet_math= move_dictionary["Skill"]["menu"]["Discreet Math"]
    switch=move_dictionary["Switch"]
    switch["name"]="eSwitch"
    defend=move_dictionary["Defend"]

    my_character=computer.get_current_character()
    target=player.get_current_character()
    target_owner=player


    o_ject={"owner": target_owner, "receiver": target}
    myself={"owner": computer, "receiver":my_character}
    health_percent=(my_character.get_curr_hp()/my_character.get_max_hp())*100

    num=randint(1,10)

    if num>3 and health_percent > 30:
        action(computer, attack, o_ject)
    elif num>1 and health_percent>30 and my_character.get_curr_mp()>10:
        action(computer,discreet_math,o_ject)
    else:
        decision=randint(1,10)
        if len(computer.get_team())>1 and decision>=5:
            for name in computer.get_team():
                if name!=my_character.get_name():
                    computer.freeze_frame()
                    myself["receiver"]=computer.get_team()[name]
                    action(computer,switch,myself)
                    break
        elif randint(1, 10)>5:
            action(computer,defend,myself)
        else:
            action(computer,attack,o_ject)

    return True


def husky_ai(computer,player,move_dictionary,action=None):

    #Moves List:
    attack=move_dictionary["Attack"]
    growl= move_dictionary["Skill"]["menu"]["Growl"]
    switch=move_dictionary["Switch"]
    switch["name"]="eSwitch"
    defend=move_dictionary["Defend"]

    my_character=computer.get_current_character()
    target=player.get_current_character()
    target_owner=player


    o_ject={"owner": target_owner, "receiver": target}
    myself={"owner": computer, "receiver":my_character}
    health_percent=(my_character.get_curr_hp()/my_character.get_max_hp())*100

    num=randint(1,10)

    if num<=2 and my_character.get_curr_mp()>10:
        action(computer,growl,o_ject)
    else:
        action(computer, attack, o_ject)

    return True

ai_dictionary={
    "Math professor": math_professor_ai,
    "Husky": husky_ai,
    "generic": careful_ai
}