#!/usr/bin/env python

from common.file_system import FileSystem
from common.player import LocalFilePlayer, SystemAudioUris
from common.rfid_reader import MFRC522Reader
from common.system_tag_store import SystemTagStore
from common.shell import Shell

rfidReader = MFRC522Reader()
player = LocalFilePlayer()
systemTagStore = SystemTagStore()

tag_id = rfidReader.read()

tagDir = FileSystem.path(FileSystem.RFID_BASE_DIR, tag_id)
if tagDir.exists():
    player.play_rfid(tag_id)
elif systemTagStore.get(tag_id) is not None:
    Shell.execute(systemTagStore.get(tag_id))
else:
    player.play_file(SystemAudioUris.SAD_TROMBONE)

rfidReader.cleanup()
