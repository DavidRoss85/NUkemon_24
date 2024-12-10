from src.units.Character import Character
from src.globals.sprites import Sprites
from src.units.subcharacters.AllPowerful import AllPowerful
from src.units.subcharacters.Brute import Brute
from src.units.subcharacters.Genius import Genius
from src.units.subcharacters.Husky import Husky
from src.units.subcharacters.LazyStudent import LazyStudent
from src.units.subcharacters.MathProfessor import MathProfessor
from src.units.subcharacters.TeachingAssistant import TeachingAssistant


class Personas:
    """
    Playable characters in the game are constructed and stored as static variables here
    """

    big_g=AllPowerful("He-Man", 10, 10, 10, 6, 6, Sprites.male_normal_backpack_behind)

    rory=LazyStudent("Rory", 1, 10, 10, 5, 5, Sprites.male_normal_backpack_behind)

    lin=Genius("Lin",1,10,10,4,6,Sprites.girl_black_hair)

    jen = Character("Jen", 1, 10, 10, 4, 6, Sprites.girl_brown_hair)

    chris=Brute("Chris", 1, 10, 10, 6, 4, Sprites.male_muscular_shirtless_behind)

    enemy1=Character("Wendie",1,200,200,5,5,Sprites.emoji_on_fire,600,200)

    enemy2=Character("Evil",1,145,100,10,10,Sprites.emoji_chill)

    math_professor_a=MathProfessor("Math Professor", 1, 200, 100, 5, 6, Sprites.professor_a)

    professor_b = Character("Professor B", 3, 200, 100, 5, 5, Sprites.professor_b)

    teaching_assistant_a = TeachingAssistant("Teach Assist A",4,150,150,4,4,Sprites.teaching_assistant_a)

    nu_husky_a= Husky("NU Husky",3,100,0,5,0,Sprites.nu_husky)

class Crews:
    """
    Default Teams comprised of personas
    """
    default_player=[
        Personas.big_g,
        # Personas.rory,
        Personas.lin,
        # Personas.chris,
        # Personas.jen
    ]
    default_enemy=[
        Personas.math_professor_a,
        Personas.professor_b,
        Personas.nu_husky_a,
        Personas.teaching_assistant_a
    ]

