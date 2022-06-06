#!/usr/bin/env python

import os
from logger import Logger


class Player:
    def play(self, uri):
        Logger.log(f"Playing {uri}")


class LocalFilePlayer(Player):
    def play(self, uri):
        super().play(uri)
        os.system("mpc -q clear")
        os.system(f"mpc -q add Files/{uri}")
        os.system("mpc -q play")
