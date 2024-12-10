import sys
import os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'../..'))

import pygame
import time
from sound import Sound

def test_play():
    pygame.init()
    sound_dict = {"boop": "boop.wav", "robot": "sound_file_robot.wav"}
    mysound = Sound(0.7, 0.8, sound_dict)

    print(mysound.get_volume())
    mysound.set_volume(0.8)
    print(mysound.get_volume())

    print(mysound.get_sounds())
    mysound.add_sound("oneup", "sound_file_one_up.wav")
    print(mysound.get_sounds())  # {'boop': 'sound_boop.wav', 'robot': 'sound_robot.wav', 'oneup': 'sound_one_up.wav'}

    mysound.play("boop")
    # mysound.play_music(start=0)

    start = time.time()

    while True:

        if time.time() >= start + 2:
            mysound.play("oneup")

        if time.time() >= (start + 5):
            break

    pygame.quit()

def test_play_music():

    sound_dict = {"boop": "boop.wav", "robot": "sound_file_robot.wav"}
    mysound = Sound(0.7,0.8, sound_dict, "victory1.ogg")


    mysound.play_music(start=0)

    start = time.time()


    while True:

        if time.time() >= start + 8:
            mysound.stop_music()

        if time.time() >= (start + 10):
            break

    pygame.quit()

if __name__=="__main__":
    test_play()
    test_play_music()
