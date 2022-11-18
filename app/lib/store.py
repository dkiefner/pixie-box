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

    def get_string(self, key):
        with dbm.open(self.__store_path, 'c') as store:
            value = store.get(str(key))
            store.close()

            if value is not None:
                return value.decode()
            else:
                return value

    def get_int(self, key):
        value = self.get_string(key)

        if value is not None:
            return int(value)
        else:
            return None

    def delete(self, key):
        Logger.log(f"Deleting {key}")
        with dbm.open(self.__store_path, 'c') as store:
            if store.get(str(key)) is not None:
                del store[str(key)]
            store.close()


class ServiceStateStore(BaseStore):
    KEY_LAST_SCANNED_RFID = "last-scanned-rfid"
    KEY_PLAYER_STOPPED_TIMESTAMP = "player_stopped_timestamp"
    KEY_SLEEP_TIMER_TIMEOUT_IN_SECONDS = "sleep_timer_timeout_in_seconds"

    def __init__(self):
        BaseStore.__init__(self, FileSystem.DATA_DIR, "service-state-store")


class SystemTagStore(BaseStore):

    def __init__(self):
        BaseStore.__init__(self, FileSystem.DATA_DIR, "system-tag-store")
