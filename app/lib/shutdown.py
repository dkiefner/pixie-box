#!/usr/bin/env python

from lib.logger import Logger
from lib.shell import Shell


class Shutdown:

    @staticmethod
    def halt():
        Logger.log("Shutting down system.")
        Shell.execute("shutdown -h now")
