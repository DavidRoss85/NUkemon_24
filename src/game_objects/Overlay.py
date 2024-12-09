from src.game_objects.Effect import Effect
from src.graphics.Sprite import Sprite


class Overlay:
    """
    Creates an object surface to draw special effects to, such as explosions.
    Special effects are Effect objects with animation frames
    """
    def __init__(self,x,y,width,height):
        self.__x=x  # x coord
        self.__y=y  # y coord
        self.__width=width  #width
        self.__height=height    #height
        self.__visible=True #toggle visibility
        self.__draw_queue=dict()    #Dictionary of effects. Will draw each item in the order it was added

        #Main sprite for rendering
        self.__sprite=Sprite(self.__x,self.__y,self.__width,self.__height,None,(0,0,0),(127,127,127))


    def get_visible(self):
        """
        :return: visibility
        """
        return self.__visible

    def get_sprite(self):
        """
        Draws the current item to the sprite and return
        :return: Object sprite
        """
        self.__draw_items_in_queue()
        return self.__sprite

    def get_x(self):
        """
        :return: x coord
        """
        return self.__x

    def get_y(self):
        """
        :return: y coord
        """
        return self.__y

    def set_visible(self,value:bool):
        """
        Toggle visibility
        :param value: Boolean (True/False)
        """
        self.__visible=value

    def set_x(self,x):
        """
        Set x coord
        :param x: x coord
        """
        self.__x=x

    def set_y(self,y):
        """
        Set y coord:
        :param y: y coord
        """
        self.__y=y

    def __draw_items_in_queue(self):
        """
        Draw the items in the draw queue
        """
        self.__sprite.restore() #Clear sprite
        if len(self.__draw_queue)<1:return  #Exit if queue empty

        for item,x,y in self.__draw_queue.values():
            #Draw routine for surfaces here
            surface=item.get_sprite().get_surface()
            self.__sprite.draw_on_surface(surface,x,y)


    def add_to_queue(self,ref,effect:Effect,x=0,y=0):
        """
        Add item to draw queue
        :param ref: key to reference object in dictionary
        :param effect: Effect object to draw
        :param x: x coord to draw at
        :param y: y coord to draw at
        """
        self.__draw_queue[ref]=list([effect,x,y])

    def remove_from_queue(self,ref):
        """
        Remove an item from queue
        :param ref: Reference key for deletion
        """
        if ref in self.__draw_queue:
            del self.__draw_queue[ref]
