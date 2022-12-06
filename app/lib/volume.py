#!/usr/bin/env python

from lib.logger import Logger


class Volume:
    def up(self):
        pass

    def down(self):
        pass

    def get(self):
        pass


class AMixerVolume(Volume):
    MIN_VALUE = 5
    MAX_VALUE = 100
    CHANGE_VALUE = 5

    def __init__(self, shell):
        self.shell = shell

    def up(self):
        current = self.get()
        Logger.log(f"Increase volume. Current level is {current}%")

        if current < self.MAX_VALUE:
            if (current + self.CHANGE_VALUE) > self.MAX_VALUE:
                self.__set(self.MAX_VALUE)
            else:
                self.__set(current + self.CHANGE_VALUE)
        else:
            Logger.log("Cannot increase volume. Maximum volume reached.")

    def down(self):
        current = self.get()
        Logger.log(f"Decrease volume. Current level is {current}%")

        if current > self.MIN_VALUE:
            if (current - self.CHANGE_VALUE) < self.MIN_VALUE:
                self.__set(self.MIN_VALUE)
            else:
                self.__set(current - self.CHANGE_VALUE)
        else:
            Logger.log(f"Cannot decrease volume. Minimum volume level of {self.MIN_VALUE}% reached.")

    def get(self):
        level = self.shell.execute(
            "amixer sget Headphone | awk -F 'Playback|[][]' 'BEGIN {RS=\"\"}{ print substr($5, 1, length($5)-1) }'")
        try:
            return int(level)
        except ValueError:
            return -1

    def __set(self, level):
        if 0 <= level <= 100:
            self.shell.execute(f"amixer set Headphone {level}%")
        else:
            Logger.log(f"Invalid volume of [{level}]. The volume level needs to be between 0 and 100.")


class FakeVolume(Volume):
    def up(self):
        Logger.log("Volume up.")

    def down(self):
        Logger.log("Volume down.")

    def get(self):
        return -50
