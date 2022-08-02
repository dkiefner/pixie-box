#!/usr/bin/env python

import dbm
import os

from common.logger import Logger


class SystemTagStore:
    __store_path = os.path.join("/home/pi/pixiebox", "system-tag-store")

    def save(self, key, value):
        Logger.log(f"Storing {key}={value}")
        with dbm.open(self.__store_path, 'c') as store:
            store[str(key)] = str(value)
            store.close()

    def get(self, key):
        with dbm.open(self.__store_path, 'r') as store:
            value = store.get(str(key)).decode()
            store.close()
            return value
