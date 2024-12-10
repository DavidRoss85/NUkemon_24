from src.game_objects.InfoBox import InfoBox


class Messenger:
    """
    This object Holds messages and handles streaming it to the input box
    """
    def __init__(self,message_box:InfoBox=None,mixer=None):
        self.__history=""   #All combined text
        self.__message_box:InfoBox=message_box  #Text box to receive stream
        self.__tick=0   #Timer
        self.__mixer=mixer  #Audio player

    def process_message(self,text:str):
        """
        Receives text and adds it to entire history
        :param text: String to add
        """
        self.__history+=text
        self.stream_text()

    def stream_text(self):
        """
        Streams text to the message box
        """
        #Increment
        self.increment_tick()
        #Cut text equivalent to tick count and send to message box
        self.__message_box.write_text(self.__history[0:self.__tick])

    def set_message_box(self,message_box):
        """
        Set the message box
        :param message_box: message box
        """
        self.__message_box=message_box

    def increment_tick(self):
        """
        Increment tick count and play sound
        Keep tick count below length of history
        """
        if self.__tick<len(self.__history)-1:
            self.__tick+=1
            if self.__mixer is not None:
                self.__mixer.play("boop")