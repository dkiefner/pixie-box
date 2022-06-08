#!/usr/bin/env python

import os

from common.file_system import FileSystem
from common.logger import Logger
from common.rfid_reader import MFRC522Reader

rfidReader = MFRC522Reader()

Logger.log(f"Move all audio files you want to associate with an RFID tag into the folder {FileSystem.UPLOAD_DIR}")
Logger.log("Scan your RFID tag now.")

tag_id = rfidReader.read()

rfidDir = FileSystem.path(FileSystem.RFID_BASE_DIR, tag_id)

Logger.log("Checking if directory already exists...")
if rfidDir.exists():
    Logger.log(f"{rfidDir} already exists. Please delete directory manually and retry!")
else:
    Logger.log(f"Creating dir {rfidDir}")
    os.mkdir(rfidDir)

    Logger.log(f"Moving files from {FileSystem.UPLOAD_DIR} to {rfidDir}")
    FileSystem.move(FileSystem.UPLOAD_DIR, rfidDir)

rfidReader.cleanup()
