from src.graphics.Sprite import Sprite


class Effect:
    def __init__(self,x,y,width,height,frames=[]):
        self.__x=x
        self.__y=y
        self.__width=width
        self.__height=height
        self.__visible=True
        self.__frames=frames #List of surfaces
        self.__frame_index=0
        self.__max_frames=len(self.__frames)


        self.__sprite=Sprite(self.__x,self.__y,self.__width,self.__height,None,(0,0,0),(127,127,127))

    def get_visible(self):
        return self.__visible

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def set_visible(self, value: bool):
        self.__visible = value

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def __paint_effect_frame(self):

        index=self.__frame_index
        if len(self.__frames)>0:
            if index> len(self.__frames)-1:
                index=len(self.__frames)-1
            frame=self.__frames[self.__frame_index]

            #Clear the current surface:
            self.__sprite.restore()
            #Draw the current frame:
            self.__sprite.draw_on_surface(
                frame.get_surface(),
                frame.get_surface().get_rect().x,
                frame.get_surface().get_rect().y
            )

    def set_frame_index(self,num):
        self.__frame_index= 0 if num>len(self.__frames)-1 else num

    def get_max_frames(self):
        return self.__max_frames

    def get_frame_index(self):
        return self.__frame_index

    def get_sprite(self):
        self.__paint_effect_frame()
        return self.__sprite

    def add_frame(self,sprite:Sprite):
        self.__frames.append(sprite)
        self.__max_frames=len(self.__frames)

    def add_multiple_frames(self,sprites:list):
        self.__frames+=sprites
        self.__max_frames=len(self.__frames)