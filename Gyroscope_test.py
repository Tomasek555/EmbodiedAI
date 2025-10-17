#!/usr/bin/env python3

from ev3dev2.sensor.lego import TouchSensor, GyroSensor

from ev3dev2.sound import Sound

from time import sleep

# Connect gyro and touch sensors to any sensor ports

gy = GyroSensor() 


sound = Sound()

# Stop program by long-pressing touch sensor button

while True:

    angle = gy.angle

    print(str(angle) + ' degrees')

    sound.play_tone(1000+angle*10, 1)

    sleep(0.5)