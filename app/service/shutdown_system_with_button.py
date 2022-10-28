#!/usr/bin/env python

import RPi.GPIO as GPIO

from lib.logger import Logger
from lib.shutdown import Shutdown

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

Logger.log("Waiting for button press...")
GPIO.wait_for_edge(3, GPIO.FALLING)

Shutdown.halt()
