#!/usr/bin/env python

import RPi.GPIO as GPIO

from lib.logger import Logger


class PowerLed:
    LED_PIN = 17

    @staticmethod
    def on():
        Logger.log("Turning on power LED.")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PowerLed.LED_PIN, GPIO.OUT)
        GPIO.output(PowerLed.LED_PIN, GPIO.HIGH)

    @staticmethod
    def off():
        Logger.log("Turning off power LED.")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PowerLed.LED_PIN, GPIO.OUT)
        GPIO.output(PowerLed.LED_PIN, GPIO.LOW)
