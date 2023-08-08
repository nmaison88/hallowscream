#!/usr/bin/python3.7
import pygame.mixer
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
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


sounds = ['onlyTakeOne.wav',
          'comeCloser.wav',
          'perfectInMyStew.wav',
          'witchLaugh.wav',
          'hahaaBoo.wav',
          'didYouJustTakeSomeCandy?.wav',
          'hahahBooMonster.wav',
          'Growl.wav',
          'getAwayFromMyHouse.wav',
          'TrickOrTreat.wav',
          'IHopeYouLike.wav',
          'Spooky.wav',
          'MonsterLaugh.wav']

dinoSounds = ['1. T-Rex Roar.wav',
              'Dino_Trex_Vox_Bite_01.wav',
              '2. T-Rex Roar.wav',
              'Dino_Trex_Vox_Bite_03.wav',
              '3. T-Rex Roar.wav',
              'Dino_Trex_Vox_Chomp_01.wav',
              '10. T-Rex Roar.wav',
              'Dino_Trex_Vox_Bite_02.wav',
              '4. T-Rex Roar.wav',
              'Dino_Trex_Vox_Bite_05.wav',
              '5. T-Rex Roar.wav',
              '6. T-Rex Roar.wav',
              '7. T-Rex Roar.wav',
              '2. T-Rex Roar.wav',
              '8. T-Rex Roar.wav',
              '9. T-Rex Roar.wav',
              'babyDinoWail.mp3',
              'Dino_Trex_Vox_Chomp_Breath_03.wav']
sound_player = pygame.mixer.Channel(2)
currentIndex = 0

print("Sampler Ready.")
sound_to_play = pygame.mixer.Sound(dirname + '/fx/' + sounds[12])
dino_sound_to_play = pygame.mixer.Sound(dirname + '/dinoFx/' + dinoSounds[12])

# sound_player.play(sound_to_play)
# sound_player.play(dino_sound_to_play)


def getMeasurement():
    # get the height of the person at the door
    print("Distance Measurement In Progress")
    GPIO.output(TRIG, False)

    print("Waiting For Sensor To Settle")
    time.sleep(2)
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
        # check if the person is tall by checking if theyre at least 4 ft from the sensor above head
        big_kid = feet_detected < 4
        print("is it a big_kid", big_kid)

        if GPIO.input(SWITCH):
            if big_kid:
                print("WE GOT A BIGGIN, SCARE EM")
                print("triggered! playing" + str(dinoSounds[currentIndex]))

                sound_to_play = pygame.mixer.Sound(
                    dirname + '/dinoFx/' + dinoSounds[currentIndex])
                sound_player.play(dino_sound_to_play)
                currentIndex = currentIndex + 1
                # Restart the index for the sounds
                if currentIndex > 16:
                    print("Starting over")
                    currentIndex = 0
            else:
                print("triggered! playing" + str(sounds[currentIndex]))
                sound_to_play = pygame.mixer.Sound(
                    dirname + '/fx/' + sounds[currentIndex])
                sound_player.play(sound_to_play)
                currentIndex = currentIndex + 1
                # Restart the index for the sounds
                if currentIndex > 12:
                    print("Starting over")
                    currentIndex = 0
            sleep(10)

    except KeyboardInterrupt:
        exit()
