from src.units.Character import Character
from src.globals.sprites import Sprites


class Personas:
    rory=Character("Rory", 1, 150, 150, 10, 10,Sprites.rory_battle1)

    mina=Character("Mina",1,100,200,10,10,Sprites.emoji_chill)

    chris=Character("Chris", 1, 200, 100, 15, 5,Sprites.rory_battle1)

    enemy1=Character("Wendie",1,200,200,5,5,Sprites.emoji_on_fire,600,200)

    enemy2=Character("Evil",1,145,100,10,10,Sprites.emoji_chill)

    professor_a=Character("Professor A",1,200,100,10,10,Sprites.professor_a)

    professor_b = Character("Professor B", 1, 200, 100, 10, 10, Sprites.professor_b)

class Crews:
    default_player=[Personas.rory,Personas.mina,Personas.chris]

    default_enemy=[Personas.professor_a, Personas.professor_b]