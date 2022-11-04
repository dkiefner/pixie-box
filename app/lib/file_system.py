#!/usr/bin/env python

import os
import pathlib

from lib.logger import Logger
from lib.shell import Shell


class FileSystem:
    ROOT_DIR = "/home/pi/pixiebox/"
    DATA_DIR = f"{ROOT_DIR}data/"
    RFID_BASE_DIR = f"{DATA_DIR}audio/rfid/"
    TEMP_DIR = f"{ROOT_DIR}tmp/"
    UPLOAD_DIR = f"{TEMP_DIR}upload/"
    SYSTEM_AUDIO_DIR = f"{ROOT_DIR}audio/system/"

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

    @staticmethod
    def save(file, path):
        FileSystem.create_path(path)
        file_path = os.path.join(path, file.filename)
        Logger.log(f"Saving file {file.filename} to {path}")
        file.save(file_path)
        return file_path

    @staticmethod
    def delete_content(directory_path):
        Logger.log(f"Deleting all content in: {directory_path}")
        Shell.execute(f"rm -rf {directory_path}*")

    @staticmethod
    def create_path(path):
        if not os.path.exists(path):
            os.makedirs(path)
