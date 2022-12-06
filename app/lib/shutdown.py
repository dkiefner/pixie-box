#!/usr/bin/env python

from lib.logger import Logger


class Shutdown:
    def halt(self):
        pass


class SystemShutdown(Shutdown):

    def __init__(self, shell):
        self.shell = shell

    def halt(self):
        Logger.log("Shutting down system.")
        self.shell.execute("shutdown -h now")


class FakeShutdown(Shutdown):
    def halt(self):
        Logger.log("Shutting down system.")
