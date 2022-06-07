#!/usr/bin/env python

import os
import pathlib

from src.common.logger import Logger

from src.common.rfid_reader import MFRC522Reader

reader = MFRC522Reader()
uploadDir = "/home/pi/pixiebox/audio/upload/"

Logger.log(f"Move all audio files you want to associate with a RFID tag into the folder {uploadDir}")
Logger.log("Scan your RFID tag now.")

tag_id = reader.read()

rfidDir = f"/home/pi/pixiebox/audio/rfid/{tag_id}/"

Logger.log("Checking if directory already exists...")
newDir = pathlib.Path(rfidDir)
if newDir.exists():
    Logger.log(f"{rfidDir} already exists. Please delete directory manually and retry!")
else:
    Logger.log(f"Creating dir {rfidDir}")
    os.mkdir(newDir)

    Logger.log(f"Moving files from {uploadDir} to {rfidDir}")
    allfiles = os.listdir(uploadDir)
    for f in allfiles:
        os.rename(uploadDir + f, rfidDir + f)
