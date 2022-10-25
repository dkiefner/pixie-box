#!/usr/bin/env python

from lib.rfid_reader import MFRC522Reader

rfidReader = MFRC522Reader()
rfidReader.read()
rfidReader.cleanup()
