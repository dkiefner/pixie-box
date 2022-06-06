#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

from logger import Logger
from player import LocalFilePlayer

reader = SimpleMFRC522()
player = LocalFilePlayer()

try:
    while True:
        Logger.log("Waiting for RFID chip...")
        chip_id = reader.read()
        Logger.log(f"id={chip_id}")

        if chip_id == 702576266227:
            player.play(chip_id)
finally:
    GPIO.cleanup()
