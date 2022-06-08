#!/usr/bin/env python

from common.file_system import FileSystem
from common.player import LocalFilePlayer, SystemAudioUris
from common.rfid_reader import MFRC522Reader

rfidReader = MFRC522Reader()
player = LocalFilePlayer()

while True:
    tag_id = rfidReader.read()

    tagDir = FileSystem.path(FileSystem.RFID_BASE_DIR, tag_id)
    if tagDir.exists():
        player.play(tag_id)
    else:
        player.play(SystemAudioUris.SAD_TROMBONE)
