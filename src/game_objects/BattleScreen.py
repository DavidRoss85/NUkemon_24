from pyexpat.errors import messages

from src.graphics.Renderer import Renderer


class BattleScreen:
    def __init__(self,player,enemy,message_box,player_menu,player_stat_box,enemy_stat_box,background,animation_layer):
        self.player=player
        self.enemy=enemy
        self.message_box=message_box
        self.player_menu=player_menu
        self.enemy_stat_box=enemy_stat_box
        self.player_stat_box=player_stat_box
        self.background=background
        self.animation_layer=animation_layer

    def create_layers(self,renderer:Renderer):
        #Add all objects to layers
        # renderer.add_to_layer(background)
        # renderer.add_to_layer(enemy,1)
        renderer.add_to_layer(self.player,1)
        # renderer.add_to_layer(enemylifbar,2)
        # renderer.add_to_layer(playerlifbar,2)
        renderer.add_to_layer(self.message_box,2)
        renderer.add_to_layer(self.player_menu,3)
        # renderer.add_to_layer(effectslayer,4)
