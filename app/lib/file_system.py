#!/usr/bin/env python

import os
import pathlib

from lib.logger import Logger


class FileSystem:
    def __init__(self, root_dir):
        self.root_dir = root_dir

    def get_data_dir(self):
        return f"{self.root_dir}data/"

    def get_rfid_base_dir(self):
        return f"{self.get_data_dir()}audio/rfid/"

    def get_temp_dir(self):
        return f"{self.root_dir}tmp/"

    def get_upload_dir(self):
        return f"{self.get_temp_dir()}upload/"

    def get_system_audio_dir(self):
        return f"{self.root_dir}audio/system/"

    def path(self, base_path, directory):
        pass

    def move(self, source, target):
        pass

    def save(self, file, path):
        pass

    def delete_content(self, directory_path):
        pass

    def create_path(self, path):
        pass


class RealFileSystem(FileSystem):

    def __init__(self, shell, root_dir):
        super().__init__(root_dir)
        self.shell = shell

    def path(self, base_path, directory):
        return pathlib.Path(f"{base_path}{directory}/")

    def move(self, source, target):
        if source[-1] != '/':
            source += '/'
        if target[-1] != '/':
            target += '/'

        Logger.log(f"Moving files from {source} to {target}")
        allfiles = os.listdir(source)
        for file in allfiles:
            Logger.log(f"Moving file: {str(file)}")
            os.rename(source + file, target + file)

    def save(self, file, path):
        self.create_path(path)
        file_path = os.path.join(path, file.filename)
        Logger.log(f"Saving file {file.filename} to {path}")
        file.save(file_path)
        return file_path

    def delete_content(self, directory_path):
        Logger.log(f"Deleting all content in: {directory_path}")
        self.shell.execute(f"rm -rf {directory_path}*")

    def create_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
