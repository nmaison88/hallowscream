#!/usr/bin/python3.7
# Imports go here
import pygame
import time
from time import sleep
from sys import exit
import os
import RPi.GPIO as GPIO
import random
# startup/initialization goes here
pygame.mixer.init(44000, -16, 1, 1024)
dirname = os.path.dirname(os.path.abspath(__file__))
SWITCH = 4
LEFT_ARM_RELAY = 23
RIGHT_ARM_RELAY = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_ARM_RELAY, GPIO.OUT)
GPIO.setup(RIGHT_ARM_RELAY, GPIO.OUT)
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
sound_player = pygame.mixer.Channel(2)
ready_sound = pygame.mixer.Sound(dirname + '/ready.mp3')
growl_sound = pygame.mixer.Sound(dirname + '/raptorFx/' + 'growl_fast.wav')
growl_sound.set_volume(.1)
dino_sound_library = ['jump',
                      'classic',
                      'call',
                      'growl',
                      'talk',
                      'attack'
                      ]
movements = ['twitch-left', 'twitch-right',
             'rise', 'fall', 'center', 'shudder']
animating = False
DELAY_SCARE = 3 # delay the scare by this amount, set to 0 for no delay
# SOUND FILES
# 'barky.wav',
# 'caw_scare_sting.wav',
# 'distant_forest.wav',
# 'growl_higher_pitch.wav',
# 'quick.wav',
# 'screech.wav',
# 'shorter_caw.wav',
# 'Longest_growl.wav',
# 'classic.wav',
# 'fast_caw.wav',
# 'growl_jump.wav',
# 'raptorsounds.19.wav',
# 'screech_caw.wav',
# 'slow_growl.wav',
# 'call_others.wav',
# 'classic3.wav',
# 'fast_growl_sting.wav',
# 'growl_medium.wav',
# 'raptorsounds.85.wav',
# 'screech_growl.wav',
# 'spike.wav',
# 'call_others2.wav',
# 'classic4.wav',
# 'goody.wav',
# 'growl_spike.wav',
# 'raptorsounds.93.wav',
# 'screech_long.wav',
# 'sting.wav',
# 'call_others3.wav',
# 'classic_bark.wav',
# 'growl.wav',
# 'longer_growl.wav',
# 'raptorsounds.70.wav',
# 'screech_longest.wav',
# 'sting2.wav',
# 'caw_distant_screech.wav',
# 'classic_wail.wav',
# 'growl_caw.wav',
# 'muffled_caw.wav',
# 'reverby.wav',
# 'screech_short.wav',
# 'wail.wav',
# 'caw_inside_space.wav',
# 'distant_caw.wav',
# 'growl_fast.wav',
# 'muffled_caw_distant.wav',
# 'scary.wav',
# 'short_caw.wav'
currentIndex = 0
dinoCurrentIndex = 0
delayScare = False
isWarmingUp = False


def playMovement(movement=''):
    if (movement == 'center'):
        GPIO.output(LEFT_ARM_RELAY, False)
        GPIO.output(RIGHT_ARM_RELAY, False)
    elif (movement == 'twitch-left'):
        GPIO.output(LEFT_ARM_RELAY, True)
        GPIO.output(RIGHT_ARM_RELAY, False)
        sleep(.5)
        GPIO.output(LEFT_ARM_RELAY, False)
        sleep(.5)
        GPIO.output(LEFT_ARM_RELAY, True)
    elif (movement == 'twitch-right'):
        GPIO.output(LEFT_ARM_RELAY, False)
        GPIO.output(RIGHT_ARM_RELAY, True)
        sleep(.5)
        GPIO.output(RIGHT_ARM_RELAY, False)
        sleep(.5)
        GPIO.output(RIGHT_ARM_RELAY, True)
    elif (movement == 'rise'):
        GPIO.output(LEFT_ARM_RELAY, False)
        GPIO.output(RIGHT_ARM_RELAY, False)
        sleep(.5)
        GPIO.output(LEFT_ARM_RELAY, True)
        GPIO.output(RIGHT_ARM_RELAY, True)
    elif (movement == 'fall'):
        GPIO.output(LEFT_ARM_RELAY, True)
        GPIO.output(RIGHT_ARM_RELAY, True)
        sleep(.5)
        GPIO.output(LEFT_ARM_RELAY, False)
        GPIO.output(RIGHT_ARM_RELAY, False)
    elif (movement == 'shudder'):
        GPIO.output(LEFT_ARM_RELAY, True)
        GPIO.output(RIGHT_ARM_RELAY, True)
        sleep(.1)
        GPIO.output(LEFT_ARM_RELAY, False)
        sleep(.1)
        GPIO.output(RIGHT_ARM_RELAY, False)
        sleep(.1)
        GPIO.output(LEFT_ARM_RELAY, True)
        GPIO.output(RIGHT_ARM_RELAY, True)
        sleep(.1)
        GPIO.output(LEFT_ARM_RELAY, False)
        sleep(.1)
        GPIO.output(RIGHT_ARM_RELAY, False)

# method for waiting until the current sound is done playing before moving on


def waitForAudioToFinishPlaying():
    while sound_player.get_busy():
        print("audio still playing")
        global animating
        if not animating:
            playMovement(random.choice(movements))
        sleep(.2)
    # playMovement(random.choice(movements))
        animating = False

    return
# method for playing sounds, pass an array and it'll trigger up or down for each


def playRoutine(sounds):
    for sound in sounds:
        file = pygame.mixer.Sound(
            dirname + '/raptorFx/' + sound)
        sound_player.play(file)
        global animating
        animating = True
        print("Playing sound: ", sound)
        # play random movement
        # playMovement(random.choice(movements))

        waitForAudioToFinishPlaying()

        # global extended  # reference the global extended variable
        # if (not extended):
        #     print("POP UP")
        #     GPIO.output(LEFT_ARM_RELAY, True)
        #     extended = True
        # else:
        #     print("DROP BACK DOWN")
        #     GPIO.output(LEFT_ARM_RELAY, False)
        #     extended = False

    # Return back to center
    playMovement('center')
    print("Routine Done")


def createRoutine(title=''):
    print("Getting routine for ", title)
    if (title == 'jump'):
        playRoutine(['goody.wav', 'scary.wav'])
    elif (title == 'talk'):
        playRoutine(['distant_forest.wav', 'quick.wav'])
    elif (title == 'attack'):
        playRoutine(['quick.wav', ' barky.wav'])
    elif (title == 'classic'):
        playRoutine(['classic_wail.wav', 'fast_caw.wav'])
    elif (title == 'call'):
        playRoutine(['call_others2.wav', 'caw_distant_screech.wav'])
    elif (title == 'growl'):
        playRoutine(['Longest_growl.wav', 'fast_caw.wav'])


# play a sound to let you know were ready!
sound_player.play(ready_sound)
waitForAudioToFinishPlaying()
# center the dino back
playMovement('center')


while True:
    try:
        # Only Trigger if the motion sensor detects movement
        if GPIO.input(SWITCH):
            # if True:
            print("Scare Start!")
            sleep(DELAY_SCARE)

            createRoutine(str(dino_sound_library[dinoCurrentIndex]))

            # Increment the current routine index
            dinoCurrentIndex = dinoCurrentIndex + 1

            # Restart the index for the sounds
            if dinoCurrentIndex == len(dino_sound_library):
                dinoCurrentIndex = 0
            # wait at least this long before next trigger default of 3-4 secs feels good
            sleep(3)
            sound_player.play(growl_sound)

            print("Ready to scare Again!")

    except KeyboardInterrupt:
        exit()
