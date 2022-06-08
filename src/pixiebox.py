#!/usr/bin/env python

from common.file_system import FileSystem
from common.logger import Logger
from common.player import LocalFilePlayer, SystemAudioUris
from common.rfid_reader import MFRC522Reader
from common.shell import Shell
from common.system_tag_store import SystemTagStore

rfidReader = MFRC522Reader()
player = LocalFilePlayer()
systemTagStore = SystemTagStore()

tag_id = rfidReader.read()

tagDir = FileSystem.path(FileSystem.RFID_BASE_DIR, tag_id)
if tagDir.exists():
    Logger.log(f"Audio tag id scanned.")
    player.play_rfid(tag_id)
else:
    cmd = systemTagStore.get(tag_id)
    if cmd is not None:
        Logger.log(f"System tag id scanned.")
        Shell.execute(cmd)
    else:
        Logger.log(f"Tag id not registered.")
        player.play_file(SystemAudioUris.SAD_TROMBONE)

rfidReader.cleanup()
