#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

from logger import Logger


class RFIDReader:
    def read(self):
        Logger.log("Waiting for RFID tag...")


class MFRC522Reader(RFIDReader):

    def __init__(self):
        self.reader = SimpleMFRC522()

    def read(self):
        try:
            tag_id, _ = self.reader.read()
            Logger.log(f"RFID tag scanned with tag_id={tag_id}")
            return tag_id
        finally:
            GPIO.cleanup()
