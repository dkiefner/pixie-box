#!/usr/bin/env python

from common.logger import Logger
from common.shell import Shell


class SystemAudioUris:
    SAD_TROMBONE = "file:///home/pi/pixiebox/audio/system/sad-trombone.wav"


class Player:
    def play_folder(self, folder_name):
        Logger.log(f"Playing folder {folder_name}")

    def play_file(self, file_uri):
        Logger.log(f"Playing file {file_uri}")


class LocalFilePlayer(Player):
    def play_folder(self, folder_name):
        super().play_folder(folder_name)
        self.__play(f"Files/rfid/{folder_name}")

    def play_file(self, file_uri):
        super().play_file(file_uri)
        self.__play(file_uri)

    def __play(self, uri):
        Shell.execute("mpc -q clear")
        Shell.execute(f"mpc -q add {uri}")
        Shell.execute("mpc -q play")
