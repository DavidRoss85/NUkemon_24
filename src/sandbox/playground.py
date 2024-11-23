from src.game_objects.InfoBox import InfoBox
from src.graphics.Sprite import Sprite
from src.graphics.Renderer import Renderer
from src.globals.UC import UC


import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = UC.screen_width
SCREEN_HEIGHT = UC.screen_height

running=True
clock=pygame.time.Clock()


renderer = Renderer(SCREEN_WIDTH,SCREEN_HEIGHT,(255,255,0))
temp_sprite=Sprite(200,400,200,200,"../assets/images/test_images/Boy_backpack1_hmmm_bk.png",(64,177,64),(0,0,200))
renderer.add_to_layer(temp_sprite)
square_sprite=Sprite(100,100,100,100,None,(200,0,0),(200,0,0))
print(square_sprite.get_mask())
renderer.add_to_layer(square_sprite,1)
text_box=InfoBox(0,568,1024,200,"Temporary text",(200,0,0))
renderer.add_to_layer(text_box.get_sprite(),1)
x=0
while running:
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

    x = x+1 if x<255 else 0
    temp_sprite.blend_color((x,0,0))

    renderer.render_all()
    renderer.flip_screen()
    clock.tick(300)