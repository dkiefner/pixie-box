#!/usr/bin/env python

from logger import Logger
from shell import Shell


class Player:
    def play(self, uri):
        Logger.log(f"Playing {uri}")


class LocalFilePlayer(Player):
    def play(self, uri):
        super().play(uri)
        Shell.execute("mpc -q clear")
        Shell.execute(f"mpc -q add Files/rfid/{uri}")
        Shell.execute("mpc -q play")
