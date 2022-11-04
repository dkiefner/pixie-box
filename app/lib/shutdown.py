#!/usr/bin/env python

from lib.logger import Logger
from lib.power_led import PowerLed
from lib.shell import Shell


class Shutdown:

    @staticmethod
    def halt():
        Logger.log("Shutting down system.")
        PowerLed.off()
        Shell.execute("shutdown -h now")
