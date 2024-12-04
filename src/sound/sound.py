import pygame

class Sound():
    """
    Sound class used for short sound effects and longer-running music \n
    sounds should be added to sound_dict, music should be loaded as music_file \n
    volume is a float in range of 0.0 to 1.0 (inclusive) \n
    sound_dict is in format {name:file} - {"beep": "beep_file.wav", "click": "click_file.ogg"}
    """

    def __init__(self, volume:float = 1, sound_dict:dict = {}, music_file:str = None):
        """constructor with optional args volume, sound_dict, music_file"""
        pygame.mixer.init()
        self.__volume = volume
        self.__sound_dict = sound_dict    # a saved library of sounds
        self.__loaded = {}    # this stores playing sounds so they can be stopped by name
        self.__music_file = music_file    # stores music file (only 1 can be played at a time)
        self.__music_volume = 0.8

    def set_volume(self, volume:float):
        """sets the volume of the mixer, pass in a float 0.0 - 1.0"""
        self.__volume = volume
        
    def get_volume(self):
        """returns the current set volume as float"""
        return self.__volume
    
    def add_sound(self, sound_name:str, sound_file:str):
        """adds a sound_name: sound_file to the sound dictionary"""
        self.__sound_dict[sound_name] = sound_file

    def get_sounds(self):
        """returns the sound dictionary"""
        return self.__sound_dict
    
    def play(self, sound_name:str):
        """plays the sound referenced by sound_name"""
        path = "../assets/sounds/"   # update this later to the UC class? ----------------------------------------<<<<

        if sound_name in self.__loaded:
            self.__loaded[sound_name].set_volume(self.__volume)
            self.__loaded[sound_name].play()
        elif sound_name in self.__sound_dict:
            self.__loaded[sound_name] = pygame.mixer.Sound( path + self.__sound_dict[sound_name] )
            self.__loaded[sound_name].set_volume(self.__volume)
            self.__loaded[sound_name].play()
        else:
            print(f"Play Error: Can't find {sound_name} in sound_dict")

    def stop(self, sound_name:str):
        """stops the playing sound by sound_name"""
        if sound_name in self.__loaded:
            self.__loaded[sound_name].stop()
        else:
            print("Stop Error: are you sure the sound_name is correct?")
        
    # methods below are specific to music. "music" is streamed from file rather than loaded 100%

    def add_music(self, music_file:str):
        """add / change the music_file"""
        self.__music_file = music_file

    def set_volume_music(self, music_volume):
        """set the volume level for music - float in 0.0 - 1.0"""
        self.__music_volume = music_volume

    def play_music(self, music_file:str = None, start:float = 0):
        """plays the music file. optional pass in music file and start point"""
        if music_file != None:
            self.__music_file = music_file

        if self.__music_file:
            path = "../assets/sounds/"   # update this later to the UC class? ----------------------------------------<<<<
            pygame.mixer.music.load( path + self.__music_file )
            pygame.mixer.music.set_volume(self.__music_volume)
            pygame.mixer.music.play(-1, start= start)   # -1 means loop indefinitely
        else:
            print("No music file loaded. Can't play music.")

    def stop_music(self):
        pygame.mixer.music.stop()

