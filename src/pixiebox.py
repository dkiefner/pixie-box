#!/usr/bin/env python

from src.common.file_system import FileSystem
from src.common.player import LocalFilePlayer, SystemAudioUris
from src.common.rfid_reader import MFRC522Reader

rfidReader = MFRC522Reader()
player = LocalFilePlayer()

while True:
    tag_id = rfidReader.read()

    tagDir = FileSystem.path(FileSystem.RFID_BASE_DIR, tag_id)
    if tagDir.exists():
        player.play(tag_id)
    else:
        player.play(SystemAudioUris.SAD_TROMBONE)
