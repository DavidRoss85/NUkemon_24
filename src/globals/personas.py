from src.units.Character import Character
from src.globals.sprites import Sprites
from src.units.subcharacters.Husky import Husky
from src.units.subcharacters.LazyStudent import LazyStudent
from src.units.subcharacters.MathProfessor import MathProfessor
from src.units.subcharacters.TeachingAssistant import TeachingAssistant


class Personas:
    """
    Characters in the game that have different attributes.
    """
    rory=LazyStudent("Rory", 1, 150, 150, 10, 10,Sprites.rory_battle1)

    mina=Character("Mina",1,100,200,5,15,Sprites.emoji_chill)

    chris=Character("Chris", 1, 200, 100, 15, 5,Sprites.rory_battle1)

    enemy1=Character("Wendie",1,200,200,5,5,Sprites.emoji_on_fire,600,200)

    enemy2=Character("Evil",1,145,100,10,10,Sprites.emoji_chill)

    math_professor_a=MathProfessor("Math Professor", 1, 200, 100, 10, 10, Sprites.professor_a)

    professor_b = Character("Professor B", 1, 200, 100, 10, 10, Sprites.professor_b)

    teaching_assistant_a = TeachingAssistant("Teach Assist A",1,150,150,5,8,Sprites.teaching_assistant_a)

    nu_husky_a= Husky("NU Husky",1,100,0,5,0,Sprites.nu_husky)

class Crews:
    """
    Teams comprised of personas
    """
    default_player=[
        Personas.rory,
        Personas.mina
        ,Personas.chris
    ]
    default_enemy=[
        Personas.math_professor_a,
        Personas.professor_b,
        Personas.nu_husky_a,
        Personas.teaching_assistant_a
    ]

