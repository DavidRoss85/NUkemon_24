from pyexpat.errors import messages

from src.graphics.Renderer import Renderer


class BattleScreen:
    def __init__(self):
        self.player=0
        self.enemy=0
        self.message_box=0
        self.player_menu=0
        self.enemy_stat_box=0
        self.player_stat_box=0
        self.background=0
        self.animation_layer=0

    def add_to_layers(self,renderer:Renderer):
        pass
        #Add all objects to layers
        # renderer.add_to_layer(background)
        # renderer.add_to_layer(enemy,1)
        # renderer.add_to_layer(player,1)
        # renderer.add_to_layer(enemylifbar,2)
        # renderer.add_to_layer(playerlifbar,2)
        # renderer.add_to_layer(messagebox,2)
        # renderer.add_to_layer(playermenu,3)
        # renderer.add_to_layer(effectslayer,4)
