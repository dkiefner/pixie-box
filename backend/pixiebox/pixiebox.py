#!/usr/bin/env python

import atexit

from common.command import SystemCommand
from common.file_system import FileSystem
from common.logger import Logger
from common.player import LocalFilePlayer, SystemAudioUris
from common.rfid_reader import MFRC522Reader
from common.system_tag_store import SystemTagStore

rfidReader = MFRC522Reader()
player = LocalFilePlayer()
systemTagStore = SystemTagStore()


def exit_handler():
    Logger.log(f"Shutting down PixieBox!")
    rfidReader.cleanup()


def read():
    tag_id = rfidReader.read()

    tag_dir = FileSystem.path(FileSystem.RFID_BASE_DIR, tag_id)
    if tag_dir.exists():
        Logger.log(f"Audio tag id scanned.")
        player.play_rfid(tag_id)
    else:
        cmd = systemTagStore.get(tag_id)
        if cmd is not None:
            Logger.log(f"System tag id scanned.")

            if SystemCommand[cmd] is SystemCommand.STOP:
                player.stop()
        else:
            Logger.log(f"Tag id not registered.")
            player.play_file(SystemAudioUris.SAD_TROMBONE)


atexit.register(exit_handler)

read()
