#!/usr/bin/env python

import dbm
import os

from lib.file_system import FileSystem
from lib.logger import Logger


class BaseStore:

    def __init__(self, path, name):
        self.__store_path = os.path.join(path, name)

    def save(self, key, value):
        Logger.log(f"Storing {key}={value}")
        with dbm.open(self.__store_path, 'c') as store:
            store[str(key)] = str(value)
            store.close()

    def get(self, key):
        with dbm.open(self.__store_path, 'c') as store:
            value = store.get(str(key))
            store.close()

            if value is not None:
                return value.decode()
            else:
                return value


class ServiceStateStore(BaseStore):
    KEY_LAST_SCANNED_RFID = "last-scanned-rfid"

    def __init__(self):
        BaseStore.__init__(self, FileSystem.DATA_DIR, "service-state-store")


class SystemTagStore(BaseStore):

    def __init__(self):
        BaseStore.__init__(self, FileSystem.DATA_DIR, "system-tag-store")
