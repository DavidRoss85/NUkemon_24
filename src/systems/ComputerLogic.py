from random import randint

def null_func(args1,args2,args3):
    pass

def careful_ai(computer,player,move_dictionary,action=null_func):
    """
    Careful AI will generally attack, but preference defense or switching when hp is low
    :param computer: computer player
    :param player: human player
    :param move_dictionary: list of available moves
    :param action: Action  function to carry out
    """
    #Moves List:
    attack=move_dictionary["Attack"]
    switch = move_dictionary["Attack"]
    if "Switch" in move_dictionary:
        switch = move_dictionary["Switch"]
        switch["name"] = "eSwitch"
    defend=move_dictionary["Defend"]

    #Characters and targets
    my_character=computer.get_current_character()
    target=player.get_current_character()
    target_owner=player

    o_ject={"owner": target_owner, "receiver": target}
    myself={"owner": computer, "receiver":my_character}
    health_percent=(my_character.get_curr_hp()/my_character.get_max_hp())*100

    #Random factor:
    num=randint(1,10)

    #Based on random factor, AI will perform actions:
    #90% chance to attack if health above 30%
    if num>1 and health_percent > 30:
        action(computer, attack, o_ject)
    else:
        # 5% chance to switch, 2.5% chance to defend and 2.5% chance to attack if health over 30%
        # Otherwise 50%, 25%, 25%
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

def berserk_ai(computer,player,move_dictionary,action=null_func):
    """
    Berserk AI will keep attacking no matter what
    :param computer: computer player
    :param player: human player
    :param move_dictionary: list of available moves
    :param action: Action  function to carry out
    """
    #Moves List:
    attack=move_dictionary["Attack"]
    switch = move_dictionary["Attack"]
    if "Switch" in move_dictionary:
        switch = move_dictionary["Switch"]
        switch["name"] = "eSwitch"
    defend=move_dictionary["Defend"]

    #Characters and targets
    my_character=computer.get_current_character()
    target=player.get_current_character()
    target_owner=player

    o_ject={"owner": target_owner, "receiver": target}
    myself={"owner": computer, "receiver":my_character}
    health_percent=(my_character.get_curr_hp()/my_character.get_max_hp())*100

    # num=randint(1,10)
    #Keep attacking
    action(computer,attack,o_ject)
    return True


def math_professor_ai(computer,player,move_dictionary,action=null_func):
    """
    Math professor has discreet math skill
    :param computer: computer player
    :param player: human player
    :param move_dictionary: list of available moves
    :param action: Action  function to carry out
    """

    #Moves List:
    attack=move_dictionary["Attack"]
    discreet_math= move_dictionary["Skill"]["menu"]["Discreet Math"]
    switch = move_dictionary["Attack"]
    if "Switch" in move_dictionary:
        switch = move_dictionary["Switch"]
        switch["name"] = "eSwitch"
    defend=move_dictionary["Defend"]

    #Characters and targets
    my_character=computer.get_current_character()
    target=player.get_current_character()
    target_owner=player

    o_ject={"owner": target_owner, "receiver": target}
    myself={"owner": computer, "receiver":my_character}
    health_percent=(my_character.get_curr_hp()/my_character.get_max_hp())*100

    num=randint(1,10)
    #Based on random factor, AI will perform actions:
    if num>3 and health_percent > 30:   #70% Chance to attack if Health over 30%
        action(computer, attack, o_ject)
    elif num>1 and health_percent>30 and my_character.get_curr_mp()>10: #Otherwise 20% chance to use discreet Math if health over 30%
        action(computer,discreet_math,o_ject)
    else:
        # 5% chance to switch, 2.5% chance to defend and 2.5% chance to attack if health over 30%
        # Otherwise 50%, 25%, 25%
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

def cs_professor_ai(computer,player,move_dictionary,action=null_func):
    """
    CS professor has Algorithms which boosts stats and has Big O notation
    :param computer: computer player
    :param player: human player
    :param move_dictionary: list of available moves
    :param action: Action  function to carry out
    """

    #Moves List:
    attack=move_dictionary["Attack"]
    algorithms= move_dictionary["Skill"]["menu"]["Algorithms"]
    n2=move_dictionary["Skill"]["menu"]["Big O Notation"]["menu"]["n^2"]
    n3=move_dictionary["Skill"]["menu"]["Big O Notation"]["menu"]["n^3"]
    switch = move_dictionary["Defend"]
    if "Switch" in move_dictionary:
        switch = move_dictionary["Switch"]
        switch["name"] = "eSwitch"
    defend=move_dictionary["Defend"]

    #Characters and targets
    my_character=computer.get_current_character()
    target=player.get_current_character()
    target_owner=player

    o_ject={"owner": target_owner, "receiver": target}
    myself={"owner": computer, "receiver":my_character}
    health_percent=(my_character.get_curr_hp()/my_character.get_max_hp())*100
    player_effects=target.get_battle_effects()
    my_effects=my_character.get_battle_effects()

    num=randint(1,10)
    #Based on random factor, AI will perform actions:
    if "smarter" not in my_effects or "stronger" not in my_effects:
        action(computer,algorithms,myself)

    elif health_percent > 40:
        if num>5 and "lagging" not in player_effects and "laggy AF" not in player_effects:   #50% Chance to use big O if Health over 30%
            vlist=[n2,n3]
            rn=randint(0,1)
            action(computer, vlist[rn], o_ject)
        else:
            action(computer,attack,o_ject)

    else:
        #When health drops low, 50% chance to switch
        if len(computer.get_team()) > 1 and num >= 5:
            for name in computer.get_team():
                if name != my_character.get_name():
                    computer.freeze_frame()
                    myself["receiver"] = computer.get_team()[name]
                    action(computer, switch, myself)
                    break
        elif num>2:
            action(computer,defend,myself)
        else:
            action(computer,attack,o_ject)

    return True


def husky_ai(computer,player,move_dictionary,action=null_func):
    """
    Husky has Growl skill
    :param computer: computer player
    :param player: human player
    :param move_dictionary: list of available moves
    :param action: Action  function to carry out
    """

    #Moves List:
    attack=move_dictionary["Attack"]
    growl= move_dictionary["Skill"]["menu"]["Growl"]
    switch = move_dictionary["Attack"]
    if "Switch" in move_dictionary:
        switch = move_dictionary["Switch"]
        switch["name"] = "eSwitch"
    defend=move_dictionary["Defend"]

    #Characters and targets
    my_character=computer.get_current_character()
    target=player.get_current_character()
    target_owner=player


    o_ject={"owner": target_owner, "receiver": target}
    myself={"owner": computer, "receiver":my_character}
    health_percent=(my_character.get_curr_hp()/my_character.get_max_hp())*100

    num=randint(1,10)
    #20% Chance to use "Growl" if enough mp
    print(f"rand = {num}")
    if num<=5 and my_character.get_curr_mp()>10:
        action(computer,growl,o_ject)
    else:
        #Otherwise attack
        action(computer, attack, o_ject)

    return True


ai_dictionary={
    "Math Professor": math_professor_ai,
    "CS Professor":cs_professor_ai,
    "Husky": husky_ai,
    "generic": careful_ai
}