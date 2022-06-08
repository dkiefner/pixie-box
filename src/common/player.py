#!/usr/bin/env python

from common.logger import Logger
from common.shell import Shell


class SystemAudioUris:
    SAD_TROMBONE = "file:///home/pi/pixiebox/audio/system/sad-trombone.wav"


class Player:
    def play(self, uri):
        Logger.log(f"Playing {uri}")


class LocalFilePlayer(Player):
    def play(self, uri):
        super().play(uri)
        Shell.execute("mpc -q clear")
        Shell.execute(f"mpc -q add {uri}")
        Shell.execute("mpc -q play")
