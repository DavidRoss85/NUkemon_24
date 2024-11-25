from src.game_objects.InfoBox import InfoBox


class Messenger:
    def __init__(self,message_box:InfoBox=None):
        self.__history=""
        self.__message_box:InfoBox=message_box
        self.__tick=0

    def process_message(self,text:str):
        self.__history+=text
        self.stream_text()

    def stream_text(self):
        self.increment_tick()
        self.__message_box.write_text(self.__history[0:self.__tick])

    def set_message_box(self,message_box):
        self.__message_box=message_box

    def increment_tick(self):
        if self.__tick<len(self.__history)-1:
            self.__tick+=1