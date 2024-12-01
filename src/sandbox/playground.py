
from src.globals.personas import Personas, Crews
from src.systems.BattleScreen import BattleScreen
from src.systems.Animator import Animator
from src.graphics.Renderer import Renderer
from src.globals.UC import UC

from src.players.Human import Player
from src.players.Computer import Computer

SCREEN_WIDTH = UC.screen_width
SCREEN_HEIGHT = UC.screen_height

renderer = Renderer(SCREEN_WIDTH,SCREEN_HEIGHT,UC.game_back_color)
animator=Animator()

player1=Player()
enemy1=Computer()
enemy1.animator=animator

player1.set_team(Crews.default_player)
enemy1.set_team(Crews.default_enemy)


battle_screen= BattleScreen(player1, enemy1, renderer, animator, 0)
battle_screen.create_layers(renderer)

# player1.get_current_character().set_max_hp(1500)
# player1.get_current_character().set_curr_hp(10)


battle_screen.start()
