import pygame
import time
from sound import Sound

pygame.init()

sound_dict = {"boop": "sound_boop.wav", "robot": "sound_robot.wav"}
mysound = Sound(0.7, sound_dict, "music_synth_level.mp3") 

print( mysound.get_volume() )
mysound.set_volume(0.8)
print( mysound.get_volume() )

print(mysound.get_sounds())
mysound.add_sound("oneup", "sound_one_up.wav")
print(mysound.get_sounds())    # {'boop': 'sound_boop.wav', 'robot': 'sound_robot.wav', 'oneup': 'sound_one_up.wav'}


mysound.play("boop")
mysound.play_music(start=20)

start = time.time()


while True:

    if time.time() >= start + 2:
        mysound.play("oneup")

    if time.time() >= start + 4:
        mysound.stop_music()

    if time.time() >= (start + 5):
        break

pygame.quit()
