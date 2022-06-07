#!/usr/bin/env python

import os
import pathlib


class FileSystem:
    RFID_BASE_DIR = f"/home/pi/pixiebox/audio/rfid/"
    UPLOAD_DIR = "/home/pi/pixiebox/audio/upload/"

    @staticmethod
    def path(base_path, directory):
        return pathlib.Path(f"{base_path}{directory}/")

    @staticmethod
    def move(source, target):
        allfiles = os.listdir(source)
        for file in allfiles:
            os.rename(source + file, target + file)
