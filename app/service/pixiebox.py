#!/usr/bin/env python

import atexit
import time

from lib.command import SystemCommand
from lib.player import LocalFilePlayer, SystemAudioUris
from lib.rfid_reader import MFRC522Reader
from lib.shutdown import Shutdown
from lib.store import *

rfidReader = MFRC522Reader()
systemTagStore = SystemTagStore()
serviceStateStore = ServiceStateStore()
player = LocalFilePlayer(serviceStateStore)


def exit_handler():
    Logger.log("Shutting down PixieBox!")
    rfidReader.cleanup()


def read():
    tag_id = rfidReader.read()
    serviceStateStore.save(ServiceStateStore.KEY_LAST_SCANNED_RFID, tag_id)

    tag_dir = FileSystem.path(FileSystem.RFID_BASE_DIR, tag_id)
    if tag_dir.exists():
        Logger.log("Audio tag id scanned.")
        player.play_rfid(tag_id)
    else:
        cmd = systemTagStore.get_string(tag_id)
        if cmd is not None:
            Logger.log(f"System tag id scanned for command: {cmd}")

            if SystemCommand[cmd] is SystemCommand.STOP:
                player.stop()
            elif SystemCommand[cmd] is SystemCommand.VOLUME_UP:
                player.volume_up()
            elif SystemCommand[cmd] is SystemCommand.VOLUME_DOWN:
                player.volume_down()
            elif SystemCommand[cmd] is SystemCommand.SHUTDOWN:
                Shutdown.halt()
            elif SystemCommand[cmd] is SystemCommand.NEXT:
                player.next()
            elif SystemCommand[cmd] is SystemCommand.PREVIOUS:
                player.prev()
        else:
            Logger.log(f"Tag {tag_id} not registered.")
            player.play_file(SystemAudioUris.SAD_TROMBONE)


atexit.register(exit_handler)

Logger.log("PixieBox started!")
player.play_file(SystemAudioUris.GAME_BOY_START_UP)

while True:
    read()
    # throttle rfid reads to once per second
    time.sleep(1)
