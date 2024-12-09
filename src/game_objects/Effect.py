from src.graphics.Sprite import Sprite


class Effect:
    """
    Special effects objects that draw at the top layer of the screen. These are animated so their "frames"
    attribute is a list of sprites to cycle through
    (Effects are essentially a list of Sprite objects that draw to its own Sprite to give the illusion
    of animation. These are drawn over the battle screen for things like explosions etc.)
    """
    def __init__(self,x,y,width,height,frames=[]):
        self.__x=x  #x coord
        self.__y=y  #y coord
        self.__width=width  #width
        self.__height=height    #height
        self.__visible=True #toggle visibility
        self.__frames=frames #List of surfaces
        self.__frame_index=0    #current animation frame
        self.__max_frames=len(self.__frames)    #gets max frames in list

        #Main surface sprite of object
        self.__sprite=Sprite(self.__x,self.__y,self.__width,self.__height,None,(0,0,0),(127,127,127))

    def get_visible(self):
        """
        Return visibility
        """
        return self.__visible

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

    def set_visible(self, value: bool):
        """
        Toggle visibility
        :param value: Boolean (True/False)
        """
        self.__visible = value

    def set_x(self, x):
        """
        Set x coord
        :param x: x coord
        """
        self.__x = x

    def set_y(self, y):
        """
        Set y coord
        :param y: y coord
        """
        self.__y = y

    def __paint_effect_frame(self):
        """
        Uses the frame index to draw the appropriate sprite animation frame
        """

        index=self.__frame_index    #Get frame index
        if len(self.__frames)>0:    #Ensure there are frames in the list
            if index> len(self.__frames)-1: #Don't exceed max frames
                index=len(self.__frames)-1
            frame=self.__frames[self.__frame_index] #get the current frame sprite

            #Clear the current surface:
            self.__sprite.restore()
            #Draw the current frame:
            self.__sprite.draw_on_surface(
                frame.get_surface(),
                frame.get_surface().get_rect().x,
                frame.get_surface().get_rect().y
            )

    def set_frame_index(self,num):
        """
        Set the current animation frame
        :param num: Frame number
        """
        self.__frame_index= 0 if num>len(self.__frames)-1 else num

    def get_max_frames(self):
        """
        :return: total number of frames in list
        """
        return self.__max_frames

    def get_frame_index(self):
        """
        :return: Current frame index
        """
        return self.__frame_index

    def get_sprite(self):
        """
        Paints the current frame and returns the resulting sprite
        :return: Effect sprite for drawing
        """
        self.__paint_effect_frame()
        return self.__sprite

    def add_frame(self,sprite:Sprite):
        """
        Add a frame to the animation list
        :param sprite: Sprite object to add to the frame list
        """
        self.__frames.append(sprite)
        self.__max_frames=len(self.__frames)

    def add_multiple_frames(self,sprites:list):
        """
        Append a list of sprites to the frame list
        :param sprites: List of Sprite objects
        """
        self.__frames+=sprites
        self.__max_frames=len(self.__frames)