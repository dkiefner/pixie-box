#!/usr/bin/env python

from src.common.rfid_reader import MFRC522Reader

rfidReader = MFRC522Reader()
rfidReader.read()
