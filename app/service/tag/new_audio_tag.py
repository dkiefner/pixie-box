#!/usr/bin/env python

import os

from lib.di import ServiceName
from lib.logger import Logger
from lib.rfid_reader import MFRC522Reader
from service.pixiebox import service_locator

rfidReader = MFRC522Reader()
file_system = service_locator.get(ServiceName.FileSystem)

Logger.log(
    f"Move all audio files you want to associate with an RFID tag into the folder {file_system.get_upload_dir()}")
Logger.log("Scan your RFID tag now.")

tag_id = rfidReader.read()

rfidDir = file_system.path(file_system.get_rfid_base_dir(), tag_id)

Logger.log("Checking if directory already exists...")
if rfidDir.exists():
    Logger.log(f"{rfidDir} already exists. Please delete directory manually and retry!")
else:
    Logger.log(f"Creating dir {rfidDir}")
    os.mkdir(rfidDir)

    file_system.move(file_system.get_upload_dir(), str(rfidDir))

rfidReader.cleanup()
