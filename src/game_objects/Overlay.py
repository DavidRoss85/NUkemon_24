from src.graphics.Sprite import Sprite


class Overlay:
    def __init__(self,x,y,width,height):
        self.__x=x
        self.__y=y
        self.__width=width
        self.__height=height
        self.__visible=True
        self.__draw_queue=[]

        self.__sprite=Sprite(self.__x,self.__y,self.__width,self.__height,None,(0,0,0),(127,127,127))

        # self.__test_sprite=Sprite(100,100,100,100,None,(1,1,1),(1,1,1))
        self.__draw_queue.append(self.__test_sprite)
        self.draw_items_in_queue()

    def get_visible(self):
        return self.__visible

    def get_sprite(self):
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

    def draw_items_in_queue(self):
        if len(self.__draw_queue)<1:return
        for item in self.__draw_queue:
            #Draw routine for surfaces here
            self.__sprite.draw_on_surface(item.get_surface(),item.get_rect().x,item.get_rect().y)
            pass

