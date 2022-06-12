#!/usr/bin/env python

from pixiebox.common.logger import Logger
from pixiebox.common.shell import Shell


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
