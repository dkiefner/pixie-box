#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

from src.common.logger import Logger
from src.common.player import LocalFilePlayer

reader = SimpleMFRC522()
player = LocalFilePlayer()

try:
    while True:
        Logger.log("Waiting for RFID chip...")
        chip_id, _ = reader.read()
        Logger.log(f"id={chip_id}")

        if chip_id == 702576266227:
            player.play(chip_id)
finally:
    GPIO.cleanup()
