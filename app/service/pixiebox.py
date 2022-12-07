#!/usr/bin/env python

import atexit
import time

from lib.command import SystemCommand
from lib.di import ServiceLocatorFactory, ServiceName
from lib.logger import Logger
from lib.player import SystemAudioUris
from lib.store import ServiceStateStore

service_locator = ServiceLocatorFactory.create()

file_system = service_locator.get(ServiceName.FileSystem)
player = service_locator.get(ServiceName.Player)
rfid_reader = service_locator.get(ServiceName.RFIDReader)
service_state_store = service_locator.get(ServiceName.ServiceStateStore)
shutdown = service_locator.get(ServiceName.Shutdown)
system_audio_uris = SystemAudioUris(file_system)
system_tag_store = service_locator.get(ServiceName.SystemTagStore)
volume = service_locator.get(ServiceName.Volume)


def exit_handler():
    Logger.log("Shutting down PixieBox!")
    rfid_reader.cleanup()


def read():
    tag_id = rfid_reader.read()
    service_state_store.save(ServiceStateStore.KEY_LAST_SCANNED_RFID, tag_id)

    tag_dir = file_system.path(file_system.get_rfid_base_dir(), tag_id)
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
            player.play_file(system_audio_uris.sad_trombose())


atexit.register(exit_handler)

Logger.log("PixieBox started!")
player.play_file(system_audio_uris.game_boy_start_up())

while True:
    read()
    # throttle rfid reads to once per second
    time.sleep(1)
