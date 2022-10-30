#!/usr/bin/env python

import dbm
import os

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

    def __init__(self):
        BaseStore.__init__(self, "/home/pi/pixiebox/data", "service-state-store")


class SystemTagStore(BaseStore):

    def __init__(self):
        BaseStore.__init__(self, "/home/pi/pixiebox/data", "system-tag-store")
