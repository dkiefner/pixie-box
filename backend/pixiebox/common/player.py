#!/usr/bin/env python

from common.logger import Logger
from common.shell import Shell


class SystemAudioUris:
    SAD_TROMBONE = "file:///home/pi/pixiebox/audio/system/sad-trombone.wav"


class Player:
    def play_rfid(self, tag_id):
        Logger.log(f"Playing RFID tag {tag_id}")

    def play_file(self, file_uri):
        Logger.log(f"Playing file {file_uri}")

    def stop(self):
        Logger.log(f"Stop playing")


class LocalFilePlayer(Player):
    VOLUME_MIN_VALUE = 10
    VOLUME_MAX_VALUE = 100
    VOLUME_CHANGE_VALUE = 10

    def play_rfid(self, tag_id):
        uri = f"Files/rfid/{tag_id}"
        super().play_rfid(uri)
        self.__play(uri)

    def play_file(self, file_uri):
        super().play_file(file_uri)
        self.__play(file_uri)

    @staticmethod
    def __play(uri):
        Shell.execute("mpc -q clear")
        Shell.execute(f"mpc -q add {uri}")
        Shell.execute("mpc -q play")

    def stop(self):
        Shell.execute("mpc -q stop")

    def volume_up(self):
        current = self.__get_volume()
        Logger.log(f"Increase volume. Current level is {current}%")

        if current < self.VOLUME_MAX_VALUE:
            if (current + self.VOLUME_CHANGE_VALUE) > self.VOLUME_MAX_VALUE:
                self.__set_volume(self.VOLUME_MAX_VALUE)
            else:
                self.__set_volume(current + self.VOLUME_CHANGE_VALUE)
        else:
            Logger.log("Cannot increase volume. Maximum volume reached.")

    def volume_down(self):
        current = self.__get_volume()
        Logger.log(f"Decrease volume. Current level is {current}%")

        if current > self.VOLUME_MIN_VALUE:
            if (current - self.VOLUME_CHANGE_VALUE) < self.VOLUME_MIN_VALUE:
                self.__set_volume(self.VOLUME_MIN_VALUE)
            else:
                self.__set_volume(current - self.VOLUME_CHANGE_VALUE)
        else:
            Logger.log(f"Cannot decrease volume. Minimum volume level of {self.VOLUME_MIN_VALUE}% reached.")

    @staticmethod
    def __get_volume():
        level = Shell.execute(
            "amixer sget Headphone | awk -F 'Playback|[][]' 'BEGIN {RS=\"\"}{ print substr($5, 1, length($5)-1) }'")
        return int(level)

    @staticmethod
    def __set_volume(level):
        if 0 <= level <= 100:
            Shell.execute(f"amixer set Headphone {level}%")
        else:
            Logger.log(f"Invalid volume of [{level}]. The volume level needs to be between 0 and 100.")
