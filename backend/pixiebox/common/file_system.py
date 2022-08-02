#!/usr/bin/env python

import os
import pathlib

from common.logger import Logger


class FileSystem:
    RFID_BASE_DIR = f"/home/pi/pixiebox/audio/rfid/"
    UPLOAD_DIR = "/home/pi/pixiebox/audio/upload/"

    @staticmethod
    def path(base_path, directory):
        return pathlib.Path(f"{base_path}{directory}/")

    @staticmethod
    def move(source, target):
        if source[-1] != '/':
            source += '/'
        if target[-1] != '/':
            target += '/'

        Logger.log(f"Moving files from {source} to {target}")
        allfiles = os.listdir(source)
        for file in allfiles:
            Logger.log(f"Moving file: {str(file)}")
            os.rename(source + file, target + file)
