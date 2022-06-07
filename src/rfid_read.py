#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    print("Waiting for RFID chip...")
    chip_id, _ = reader.read()
    print(chip_id)
finally:
    GPIO.cleanup()
