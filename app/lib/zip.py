#!/usr/bin/env python

import pathlib
import shutil

from lib.logger import Logger


class Zip:

    @staticmethod
    def create_from_directory(path_to_directory, filename):
        Logger.log(f"Creating zip file: {filename}.zip of content in {path_to_directory}")
        shutil.make_archive(filename, format="zip", root_dir=path_to_directory)

        return pathlib.Path(f"{filename}.zip")

    @staticmethod
    def unzip(zip_file_path, target_path):
        shutil.unpack_archive(zip_file_path, target_path)
