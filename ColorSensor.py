#!/usr/bin/env python3

import ev3dev.ev3 as ev3

clRight = ev3.ColorSensor('in1')

assert clRight.connected, "Connect a color sensor to port 1"

clRight.mode = 'COL-REFLECT'
while True:
    print("Left color sensor value: ", clRight.value())