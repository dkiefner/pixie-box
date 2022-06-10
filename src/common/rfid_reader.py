#!/usr/bin/env python

import RPi.GPIO as GPIO
from common.logger import Logger
from mfrc522 import SimpleMFRC522


class RFIDReader:
    def read(self):
        Logger.log("Waiting for RFID tag...")

    def cleanup(self):
        pass


class MFRC522Reader(RFIDReader):

    def __init__(self):
        self.reader = SimpleMFRC522()

    def read(self):
        try:
            tag_id = self.reader.read_id()
            Logger.log(f"RFID tag scanned with tag_id={tag_id}")
            return tag_id
        except:
            self.cleanup()

    def cleanup(self):
        GPIO.cleanup()
