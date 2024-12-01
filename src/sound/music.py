import pygame

class Music():
    """This should be used for continuous music rather than sound effects"""
    
    def __init__(self, music_file: str):
        pygame.mixer.init()
        self.music_file = music_file
        pygame.mixer.music.load(self.music_file)

    def play(self):
        pygame.mixer.music.play(-1) # -1 means loop indefinitely

    def stop(self):
        pygame.mixer.music.stop()


# create instance with the sound file as the argument
# example:  music_background = Music("music_file_synth_level.mp3")
# the play method should be called before the game running while loop
# not called in the game while loop
