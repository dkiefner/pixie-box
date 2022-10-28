#!/usr/bin/env python

import os
import pathlib

from lib.logger import Logger


class FileSystem:
    ROOT_DIR = "/home/pi/pixiebox/"
    DATA_DIR = f"{ROOT_DIR}data/"
    RFID_BASE_DIR = f"{DATA_DIR}audio/rfid/"
    UPLOAD_DIR = f"{DATA_DIR}audio/upload/"
    TEMP_DIR = f"{ROOT_DIR}tmp/"

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
