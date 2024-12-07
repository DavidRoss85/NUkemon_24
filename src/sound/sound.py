from src.globals.UC import UC

import pygame

class Sound:
    """
    Sound class used for short sound effects and longer-running music \n
    sounds should be added to sound_dict, music should be loaded as music_file \n
    volume is a float in range of 0.0 to 1.0 (inclusive) \n
    sound_dict is in format {name:file} - {"beep": "beep_file.wav", "click": "click_file.ogg"}
    """

    def __init__(self, effect_volume:float = 0.8, music_volume:float=0.8, sound_dict:dict = {}, music_file:str = None):
        """constructor with optional args volume, sound_dict, music_file"""
        pygame.mixer.init()
        self.__volume = effect_volume  #Sound effect volume
        self.__sound_dict = sound_dict    # a saved library of sounds
        self.__loaded = {}    # this stores playing sounds so they can be stopped by name
        self.__music_file = None    # stores music file (only 1 can be played at a time)
        self.__music_volume = music_volume  # Default music volume 80%
        self.__music_repeat_time=0

        self.__sound_path=UC.sound_path
        self.__music_path=UC.music_path
        self.__sound_effect_path=UC.se_path

        self.load_music(music_file)

    def set_sound_path(self,path):
        """
        Sets the sound path location
        :param path: Path to sound directory
        """
        self.__sound_path=path

    def set_music_path(self,path):
        """
        Sets the music path location
        :param path: Path to music directory
        """
        self.__music_path = path

    def set_sound_effect_path(self,path):
        """
        Sets the sound effect path location
        :param path: Path to sound effect directory
        """
        self.__sound_effect_path = path

    def set_volume(self, volume:float):
        """
        Sets the volume of the mixer
        :param volume: Float 0.0 - 1.0
        """
        self.__volume = volume
        
    def get_volume(self):
        """
        :return: The current set volume as float
        """
        return self.__volume
    
    def add_sound(self, sound_name:str, sound_file:str):
        """
        Adds a sound to the dictionary
        :param sound_name: Dictionary key
        :param sound_file: File name
        """
        self.__sound_dict[sound_name] = sound_file

    def remove_sound(self,sound_name:str):
        """
        Delete a sound from the dictionary
        :param sound_name: Reference to the key in the sound dictionary
        """
        if sound_name in self.__sound_dict:
            del self.__sound_dict[sound_name]
        if sound_name in self.__loaded:
            del self.__loaded[sound_name]

    def get_sounds(self):
        """
        :return: The sound dictionary
        """
        return self.__sound_dict

    def load_all_sound_effects(self):
        """
        Loads all sound files from sound dict
        """
        path= self.__sound_effect_path
        for sound_name in self.__sound_dict:
            self.__loaded[sound_name] = pygame.mixer.Sound( path + self.__sound_dict[sound_name] )
            self.__loaded[sound_name].set_volume(self.__volume)

    def play(self, sound_name:str):
        """
        Plays the sound in dictionary
        :param sound_name: key reference from sound dictionary
        """
        path = self.__sound_effect_path

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
        """
        Stops playing a specific sound
        :param sound_name: Key reference from sound dictionary
        """
        if sound_name in self.__loaded:
            self.__loaded[sound_name].stop()
        else:
            print("Stop Error: are you sure the sound_name is correct?")
        
    # methods below are specific to music. "music" is streamed from file rather than loaded 100%

    def load_music(self, music_file:str):
        """
        Add / change the music file
        :param music_file: name of music file
        :return:
        """

        path = self.__music_path  # Location of sound files
        if music_file is not None and path is not None:
            self.__music_file = music_file
            pygame.mixer.music.load( path + music_file )

    def unload_music(self):
        """
        Free up memory by unloading music
        """
        self.__music_file=None
        pygame.mixer.music.unload()

    def set_volume_music(self, music_volume):
        """
        Set the volume level for music
        :param music_volume: float 0.0 - 1.0
        :return:
        """
        self.__music_volume = music_volume

    def play_music(self, music_file:str = None, start:float = 0, repeat_time:float=0):
        """
        Plays music file loaded
        :param music_file: name of music file
        :param start: timestamp to start playing music at
        :param repeat_time: time signature to start when repeat
        :return:
        """
        self.__music_repeat_time=repeat_time
        if music_file is not None:
            self.load_music(music_file)

        if self.__music_file:
            pygame.mixer.music.set_volume(self.__music_volume)
            pygame.mixer.music.play(start= start)   # -1 means loop indefinitely
            pygame.mixer.music.set_endevent(UC.MUSIC_EVENT_END)

        else:
            print("No music file loaded. Can't play music.")

    def repeat_music(self):
        if self.__music_file:
            pygame.mixer.music.set_volume(self.__music_volume)
            pygame.mixer.music.play(start=self.__music_repeat_time)  # -1 means loop indefinitely
            pygame.mixer.music.set_endevent(UC.MUSIC_EVENT_END)

    def stop_music(self):
        """
        Stop playing music
        """
        pygame.mixer.music.stop()

