#!/usr/bin/python3.7
import pygame
import time
from time import sleep
from sys import exit
import os
import RPi.GPIO as GPIO

pygame.mixer.init(44000, -16, 1, 1024)
dirname = os.path.dirname(os.path.abspath(__file__))
SWITCH = 21
TRIG = 23
ECHO = 24
RELAY = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(RELAY, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


sounds = ['onlyTakeOne.wav',
          'comeCloser.wav',
          'perfectInMyStew.wav',
          'witchLaugh.wav',
          'hahaaBoo.wav',
          'didYouJustTakeSomeCandy?.wav',
          'hahahBooMonster.wav',
          'getAwayFromMyHouse.wav',
          'TrickOrTreat.wav',
          'IHopeYouLike.wav',
          'Spooky.wav',
          'MonsterLaugh.wav',
          'didYouJustTakeSomeCandy?.wav',
          ]

dinoSounds = ['chomp2.wav',
              'bite1.wav',
              'roar1.wav',
              'roar2.wav',
              'bite3.wav',
              'roar3.wav',
              'chomp1.wav',
              'roar10.wav',
              'bite2.wav',
              'roar4.wav',
              'bite4.wav',
              'roar5.wav',
              'roar6.wav',
              'roar7.wav',
              'roar2.wav',
              'roar8.wav',
              'roar9.wav',
              'babyDinoWail.wav',
              'chomp2.wav']
sound_player = pygame.mixer.Channel(2)
currentIndex = 0

print("Sampler Ready.")
# sound_to_play = pygame.mixer.Sound(dirname + '/fx/' + sounds[12])
# dino_sound_to_play = pygame.mixer.Sound(dirname + '/dinoFx/' + dinoSounds[12])
ready_sound = pygame.mixer.Sound(dirname + '/ready.mp3')

sound_player.play(ready_sound)


def getMeasurement():
    # get the height of the person at the door
    print("Distance Measurement In Progress")
    GPIO.output(TRIG, False)

    print("Waiting For Sensor To Settle")
    time.sleep(1)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    cm = round(distance, 2)

    inches = 0.394*cm
    feet = 0.0328*cm
    print("The length in inches", round(inches, 2))
    print("The length in feet", round(feet, 2))
    return round(feet, 2)


while True:
    try:
        feet_detected = getMeasurement()
        # check if the person is tall by checking if they're at least 4 ft from the sensor above head
        big_kid = feet_detected < 4
        print("is it a big_kid", big_kid)

        if GPIO.input(SWITCH):
            if big_kid:
                print("WE GOT A BIGGIN, SCARE EM")
                GPIO.output(RELAY, True)
                print("DINO SCARE!")

                print("triggered! playing " + str(dinoSounds[currentIndex]))

                sound_to_play = pygame.mixer.Sound(
                    dirname + '/dinoFx/' + dinoSounds[currentIndex])
                sound_player.play(sound_to_play)

                # wait until the sound is over before moving the relay back
                while sound_player.get_busy():
                    print("audio still playing")
                    sleep(1)

                print("audio done playing")
                GPIO.output(RELAY, False)
                print("DINO HIDE!")

                currentIndex = currentIndex + 1
                # Restart the index for the sounds
                if currentIndex > 18:
                    print("Starting over")
                    currentIndex = 0
            else:
                print("triggered! playing " + str(sounds[currentIndex]))
                sound_to_play = pygame.mixer.Sound(
                    dirname + '/fx/' + sounds[currentIndex])
                sound_player.play(sound_to_play)
                currentIndex = currentIndex + 1
                # Restart the index for the sounds
                if currentIndex > 12:
                    print("Starting over")
                    currentIndex = 0
            sleep(5)

    except KeyboardInterrupt:
        exit()
