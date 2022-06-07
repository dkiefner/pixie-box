#!/usr/bin/env python

from src.common.rfid_reader import MFRC522Reader
from src.common.player import LocalFilePlayer

rfidReader = MFRC522Reader()
player = LocalFilePlayer()

while True:
    tag_id = rfidReader.read()

    if tag_id == 702576266227:
        player.play(tag_id)
