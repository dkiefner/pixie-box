#!/usr/bin/env python

import RPi.GPIO as GPIO

from common.logger import Logger
from common.shell import Shell

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

Logger.log("Waiting for button press...")
GPIO.wait_for_edge(3, GPIO.FALLING)

Logger.log("Shutting down system.")
Shell.execute("shutdown -h now")
