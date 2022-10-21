#!/usr/bin/env python

import atexit
import time

from common.command import SystemCommand
from common.file_system import FileSystem
from common.logger import Logger
from common.player import LocalFilePlayer, SystemAudioUris
from common.rfid_reader import MFRC522Reader
from common.store import *

rfidReader = MFRC522Reader()
systemTagStore = SystemTagStore()
serviceStateStore = ServiceStateStore()
player = LocalFilePlayer(serviceStateStore)


def exit_handler():
    Logger.log("Shutting down PixieBox!")
    rfidReader.cleanup()


def read():
    tag_id = rfidReader.read()

    tag_dir = FileSystem.path(FileSystem.RFID_BASE_DIR, tag_id)
    if tag_dir.exists():
        Logger.log("Audio tag id scanned.")
        player.play_rfid(tag_id)
    else:
        cmd = systemTagStore.get(tag_id)
        if cmd is not None:
            Logger.log(f"System tag id scanned for command: {cmd}")

            if SystemCommand[cmd] is SystemCommand.STOP:
                player.stop()
            elif SystemCommand[cmd] is SystemCommand.VOLUME_UP:
                player.volume_up()
            elif SystemCommand[cmd] is SystemCommand.VOLUME_DOWN:
                player.volume_down()
        else:
            Logger.log("Tag id not registered.")
            player.play_file(SystemAudioUris.SAD_TROMBONE)


atexit.register(exit_handler)

Logger.log("PixieBox started!")

while True:
    read()
    # throttle rfid reads to once per second
    time.sleep(1)
