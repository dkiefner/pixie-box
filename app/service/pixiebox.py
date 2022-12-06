#!/usr/bin/env python

import atexit
import time

from lib.command import SystemCommand
from lib.di import ServiceLocatorFactory, ServiceName
from lib.file_system import FileSystem
from lib.logger import Logger
from lib.player import SystemAudioUris
from lib.rfid_reader import MFRC522Reader
from lib.store import ServiceStateStore

service_locator = ServiceLocatorFactory.create()

rfid_reader = MFRC522Reader()
player = service_locator.get(ServiceName.Player)
service_state_store = service_locator.get(ServiceName.ServiceStateStore)
shutdown = service_locator.get(ServiceName.Shutdown)
system_tag_store = service_locator.get(ServiceName.SystemTagStore)
volume = service_locator.get(ServiceName.Volume)


def exit_handler():
    Logger.log("Shutting down PixieBox!")
    rfid_reader.cleanup()


def read():
    tag_id = rfid_reader.read()
    service_state_store.save(ServiceStateStore.KEY_LAST_SCANNED_RFID, tag_id)

    tag_dir = FileSystem.path(FileSystem.RFID_BASE_DIR, tag_id)
    if tag_dir.exists():
        Logger.log("Audio tag id scanned.")
        player.play_rfid(tag_id)
    else:
        cmd = system_tag_store.get_string(tag_id)
        if cmd is not None:
            Logger.log(f"System tag id scanned for command: {cmd}")

            if SystemCommand[cmd] is SystemCommand.STOP:
                player.stop()
            elif SystemCommand[cmd] is SystemCommand.VOLUME_UP:
                volume.up()
            elif SystemCommand[cmd] is SystemCommand.VOLUME_DOWN:
                volume.down()
            elif SystemCommand[cmd] is SystemCommand.SHUTDOWN:
                shutdown.halt()
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
