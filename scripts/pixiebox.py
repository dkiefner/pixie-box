#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import os

reader = SimpleMFRC522()

try:
    while True:
        print("Waiting for RFID chip...")
        id, text = reader.read()
        print("id=",id)

        if id == 702576266227:
            print("Playing Louis")
            os.system("mpc -q clear")
            os.system("mpc -q add \"Files/702576266227\"")
            os.system("mpc -q play")
finally:
    GPIO.cleanup()
