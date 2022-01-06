#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B
from ev3dev2.motor import SpeedPercent, MoveTank
from ev3dev2.motor import MediumMotor, OUTPUT_D

from ev3dev2.sensor import INPUT_1 
from ev3dev2.sensor.lego import InfraredSensor

from ev3dev2.led import Leds
from ev3dev2.button import Button
from ev3dev2.display import Display
from textwrap import wrap
from ev3dev2.sound import Sound

from time import sleep
from threading import Thread

frontLegs = LargeMotor(OUTPUT_A)
backLegs = LargeMotor(OUTPUT_B)

steering = MediumMotor(OUTPUT_D)

ir = InfraredSensor(INPUT_1)



# Indicated sput is up and running

sound = Sound()
sound.play_tone(500, 0.5,play_type = 1)



mode = "remote"
modeArray = ["remote","auto","dance","program"]

leds = Leds()
lcd = Display()
btn = Button()

def show_text(string, font_name='courB24', font_width=15, font_height=24):
    lcd.clear()
    strings = wrap(string, width=int(180/font_width))
    for i in range(len(strings)):
        x_val = 89-font_width/2*len(strings[i])
        y_val = 63-(font_height+1)*(len(strings)/2-i)
        lcd.text_pixels(strings[i], False, x_val, y_val, font=font_name)
    lcd.update()

def btnPressed(side):
    sound.play_tone(500, 0.5,play_type = 1)
    leds.set_color(side, (0, 1)) # Bright green.
    sleep(0.25)
    leds.all_off()

def changeModes():
    global mode
    global modeArray
    length = len(modeArray)
    currentIndex = modeArray.index(mode)

    show_text(mode)

    while not btn.backspace:
        if btn.left:
            
            currentIndex -= 1

            if currentIndex == -1:
                currentIndex = length - 1

            mode = modeArray(currentIndex)
            
            btnPressed("LEFT")
            show_text(mode)

        elif btn.right:
            currentIndex += 1

            if currentIndex == 4:
                currentIndex = 0

            mode = modeArray(currentIndex)

            btnPressed("RIGHT")
            show_text(mode)

        sleep(0.25)

changeModeThread = Thread(target=changeModes)
changeModeThread.start()



steeringPos = 0
rightSwitch = 1
leftSwitch = 1

def TurnRight(state):
    global steeringPos
    
    if state and steeringPos < 180 :  
        steering.on_for_degrees(SpeedPercent(100), 180,brake = True, block = True)
        steeringPos += 180

def TurnLeft(state):
    global steeringPos
    
    if state and steeringPos > -180 :
        steering.on_for_degrees(SpeedPercent(100), -180,brake = True, block = True)
        steeringPos -= 180


ir.on_channel1_top_right = TurnRight
ir.on_channel1_top_left = TurnLeft


instructions = [
    "forward 1",
    "right",
    "left"
]

def program():




while True: 
    if mode == "remote":
        ir.process()
        

        print(ir.proximity)

        if not ir.beacon(channel = 1) and not ir.bottom_right(channel = 1):
            frontLegs.off()
            backLegs.off()
        
        if ir.beacon(channel = 1):
            frontLegs.on(speed=-75)
            backLegs.on(speed=75)
        elif ir.bottom_right(channel = 1):
            frontLegs.on(speed= 50)
            backLegs.on(speed=-50 )

    elif mode == "auto":
        frontLegs.off()
        backLegs.off()

        


    elif mode == "dance":
        frontLegs.off()
        backLegs.off()
        while mode == "dance":
            if mode != "dance":
                break
            frontLegs.on_for_rotations(SpeedPercent(50),0.5,brake=False,block = True)
            if mode != "dance":
                break
            frontLegs.on_for_rotations(SpeedPercent(50),-0.5,brake=False,block = True)
            if mode != "dance":
                break
            sound.play_tone(500, 0.5,play_type = 1)
            if mode != "dance":
                break
            sound.play_tone(500, 0.5,play_type = 1)

    elif mode == "program"
        program()
            
    sleep(1)
    # sleep(0.01)


