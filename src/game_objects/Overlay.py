from src.game_objects.Effect import Effect
from src.graphics.Sprite import Sprite


class Overlay:
    def __init__(self,x,y,width,height):
        self.__x=x
        self.__y=y
        self.__width=width
        self.__height=height
        self.__visible=True
        self.__draw_queue=dict()

        self.__sprite=Sprite(self.__x,self.__y,self.__width,self.__height,None,(0,0,0),(127,127,127))

        # self.__test_sprite=Sprite(100,100,100,100,None,(1,1,1),(1,1,1))
        # self.__draw_queue.append(self.__test_sprite)
        # self.__draw_items_in_queue()

    def get_visible(self):
        return self.__visible

    def get_sprite(self):
        self.__draw_items_in_queue()
        return self.__sprite

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def set_visible(self,value:bool):
        self.__visible=value

    def set_x(self,x):
        self.__x=x

    def set_y(self,y):
        self.__y=y

    def __draw_items_in_queue(self):
        self.__sprite.restore()
        if len(self.__draw_queue)<1:return
        for item,x,y in self.__draw_queue.values():
            #Draw routine for surfaces here
            surface=item.get_sprite().get_surface()
            self.__sprite.draw_on_surface(surface,x,y)


    def add_to_queue(self,ref,effect:Effect,x=0,y=0):
        self.__draw_queue[ref]=list([effect,x,y])

    def remove_from_queue(self,ref):
        if ref in self.__draw_queue:
            del self.__draw_queue[ref]
