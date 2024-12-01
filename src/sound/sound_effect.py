import pygame

class Sound_effect(pygame.mixer.Sound):
    """this should be used for sound effects rather than continuous music"""

    def __init__(self, sound_file: str):
        pygame.mixer.init()
        self.sound_file = sound_file

    def play(self):
        pygame.mixer.Sound(self.sound_file).play()


# create instance with the sound file as the argument
# example:  boop_sound = Sound_effect("sound_file_boop.wav")
# the play method should be called at the event causing the sound effect