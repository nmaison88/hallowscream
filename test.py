#!/usr/bin/python3.7
# Imports go here
import pygame
import time
from time import sleep
from sys import exit
import os
# import RPi.GPIO as GPIO
import cv2
import numpy as np


# startup/initialization goes here
pygame.mixer.init(44000, -16, 1, 1024)
dirname = os.path.dirname(os.path.abspath(__file__))
SWITCH = 21
TRIG = 23
ECHO = 24
RELAY = 20
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(TRIG, GPIO.OUT)
# GPIO.setup(RELAY, GPIO.OUT)
# GPIO.setup(ECHO, GPIO.IN)
# GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
sound_player = pygame.mixer.Channel(2)
ready_sound = pygame.mixer.Sound(dirname + '/ready.mp3')
dino_sound_library = ['chomp2.wav',
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
currentIndex = 0
dinoCurrentIndex = 0
extended = False

# method for waiting until the current sound is done playing before moving on
def waitForAudioToFinishPlaying():
    while sound_player.get_busy():
        print("audio still playing")
        sleep(.2)
    return
# method for playing sounds, pass an array and it'll trigger up or down for each


def playRoutine(sounds):
    for sound in sounds:
        file = pygame.mixer.Sound(
            dirname + '/dinoFx/' + sound)
        sound_player.play(file)
        print("Playing sound: ", sound)

        waitForAudioToFinishPlaying()
        print("POP Based On status")
        global extended  # reference the global extended variable
        if (not extended):
            print("POP UP")
            # GPIO.output(RELAY, True)
            extended = True
        else:
            print("DROP BACK DOWN")
            # GPIO.output(RELAY, False)
            extended = False
    print("Routine Done")


def createRoutine(title=''):
    print("Getting routine for ", title)
    if (title == 'chomp1.wav'):
        playRoutine(['roar9.wav', 'chomp1.wav'])
    if (title == 'chomp2.wav'):
        playRoutine(['bite2.wav', 'chomp2.wav'])
    elif (title == 'bite1.wav'):
        playRoutine(['bite1.wav', 'bite4.wav'])
    elif (title == 'bite2.wav'):
        playRoutine(['bite4.wav', 'bite2.wav'])
    elif (title == 'bite3.wav'):
        playRoutine(['bite3.wav', 'chomp1.wav'])
    elif (title == 'bite4.wav'):
        playRoutine(['chomp2.wav', 'bite4.wav'])
    elif (title == 'babyDinoWail.wav'):
        playRoutine(['babyDinoWail.wav', 'bite2.wav'])
    elif (title == 'roar1.wav'):
        playRoutine(['roar1.wav', 'chomp1.wav'])
    elif (title == 'roar2.wav'):
        playRoutine(['roar2.wav', 'bite3.wav'])
    elif (title == 'roar3.wav'):
        playRoutine(['roar3.wav', 'chomp2.wav'])
    elif (title == 'roar4.wav'):
        playRoutine(['roar4.wav', 'chomp2.wav'])
    elif (title == 'roar5.wav'):
        playRoutine(['roar5.wav', 'chomp1.wav'])
    elif (title == 'roar6.wav'):
        playRoutine(['roar6.wav', 'bite2.wav'])
    elif (title == 'roar7.wav'):
        playRoutine(['roar7.wav', 'bite3.wav'])
    elif (title == 'roar8.wav'):
        playRoutine(['roar8.wav', 'bite4.wav'])
    elif (title == 'roar9.wav'):
        playRoutine(['roar9.wav', 'chomp1.wav'])
    elif (title == 'roar10.wav'):
        playRoutine(['roar10.wav', 'bite1.wav'])


# play a sound to let you know were ready!
sound_player.play(ready_sound)
waitForAudioToFinishPlaying()

HEIGHT = 480
WIDTH = 640
FPS = 30.0
VIDEOCOUNT = 0


while True:
    try:
        # Only Trigger if the motion sensor detects movement
        # if GPIO.input(SWITCH):
        if True:
             
            cap = cv2.VideoCapture(0, cv2.CAP_ANY)
            cap.set(cv2.CAP_PROP_FPS, FPS)
            cap.set(cv2.CAP_PROP_CONVERT_RGB , 1)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 100)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            # output parameters such as fps and size can be changed
            output = cv2.VideoWriter(str(VIDEOCOUNT) + ".mp4", fourcc, FPS, (WIDTH, HEIGHT))
            VIDEOCOUNT += 1
            if cap.isOpened():
                (ret, frame) = cap.read()
                if ret:
                    output.write(frame)
                cv2.imshow("frame", frame)

            
            createRoutine(str(dino_sound_library[dinoCurrentIndex]))

            # Increment the current routine index
            dinoCurrentIndex = dinoCurrentIndex + 1

            # Restart the index for the sounds
            if dinoCurrentIndex > 18:
                print("Starting over")
                dinoCurrentIndex = 0
            
           
            # wait at least this long before next trigger default of 3-4 secs feels good
            sleep(3)
            output.release()
            cap.release()
            cv2.destroyAllWindows()

    except KeyboardInterrupt:
        exit()
