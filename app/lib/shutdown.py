#!/usr/bin/env python

from lib.logger import Logger
from lib.shell import Shell


class Shutdown:
    def halt(self):
        pass


class SystemShutdown(Shutdown):
    def halt(self):
        Logger.log("Shutting down system.")
        Shell.execute("shutdown -h now")


class FakeShutdown(Shutdown):
    def halt(self):
        Logger.log("Shutting down system.")
