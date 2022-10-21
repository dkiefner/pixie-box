#!/usr/bin/env python

import RPi.GPIO as GPIO

from common.logger import Logger
from common.shell import Shell

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def listen_for_button_press(on_button_pressed):
    Logger.log("Waiting for button press...")
    GPIO.wait_for_edge(3, GPIO.FALLING)
    on_button_pressed()


def shutdown_system():
    Logger.log("Shutting down system.")
    Shell.execute("shutdown -h now")


listen_for_button_press(shutdown_system)
